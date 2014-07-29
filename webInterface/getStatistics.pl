#!c:/Perl/bin/perl.exe

# includes
use CGI qw/-tabindex -nosticky :all/;
use POSIX qw(ceil floor);
use Fcntl qw(:flock);
use Cwd;
use XML::Simple;
use Time::Local;
use File::Find;
use Storable;

require('F:\bvm\CGI\Common.pl');

# Defines the current working directory and config file path
my @g_BVM_TEAM = ('David.Ju@amd.com', 'Bob.Yang@amd.com', 'Roger.Gu@amd.com','Renbo.Jiang@amd.com','You.Zhang@amd.com');



getStatics();

sub IsBVMTeamMember
{
	my $user = $_[0];
	foreach(@g_BVM_TEAM)
	{
		if($user eq $_)
		{
			return 1;
		}
	}
	return 0;
}

sub initailENV
{
	$req_dir = "F:\\bvm-dev\\BDB\\REQFORM";
	$monthInSec = 3600 * 24 * 30;
	$log= 'F:\clean-guide\getStaticsLog.txt';
	
	my %yearStatic;
	my %halfYearStatic;
	my %monthStatic;
	my %userStatic;
	my %platformStatic;
	my %summaryStatic;
	
	$halfYearRef = \%halfYearStatic;
	$monthRef = \%monthStatic;
	$yearRef = \%yearStatic;
	$userReference = \%userStatic;	
	$platformReference = \%platformStatic;
	
	$total_cbs = 0;
	$total_reg = 0;
	$total_oprom = 0;
	$total_smu = 0;
	$total_pmu = 0;
	$total_psp = 0;
	$total_ucode = 0;
	$total_samu = 0;
	
	$platformStatistics = "F:\\clean-guide\\monthStatistics.txt";
	$monthStatistics = "F:\\clean-guide\\PlatformStatistics.txt";
	$yearStatistics = "F:\\clean-guide\\YearStatistics.txt";
	$halfYearStatistics = "F:\\clean-guide\\HalfYearStatistics.txt";
	$userStatistics = "F:\\clean-guide\\UserStatistics.txt";
	$summaryStatistics = "F:\\clean-guide\\SummaryStatistics.txt";

	# $yearRef = retrieve($yearStatistics);
    # $halfYearRef = retrieve($halfYearStatistics);
    # $monthRef = retrieve($monthStatistics);
    # $userReference = retrieve($userStatistics);
    # $platformReference = retrieve($platformStatistics);	
}

sub getStatics
{

	initailENV();
	chdir $req_dir;
	my @requests_list = glob "*.xml";
	@requests_list = sort {$b cmp $a} @requests_list;

  	if (scalar(@requests_list) != 0)
	{

		appendLog("start calculate the statistic!!");
		foreach (@requests_list)
		{
		    $request = $_;
			if( isWantedFile($request,$monthInSec) )
			{
				getOneRequestStatistic($request);	
			}
			
		}
		output();
		appendLog("Successfully generate the xml results!!");					
	} 
}


sub output{
		store($platformReference,$platformStatistics);
		store($monthRef,$monthStatistics);
		store($yearRef,$yearStatistics);
		store($halfYearRef,$halfYearStatistics);
		store($userReference,$userStatistics);
		store(\%summaryStatic,$summaryStatistics);
}


sub appendLog{
    my $text = shift;
    open (LOG_FILE, ">>",$log) or print "Cannot open $log for write.";
    print LOG_FILE $text."\n\n";
    print $text."\n";
    close LOG_FILE;
}

sub isWantedFile{
    my $file = shift;
    my $timeLimited = shift;
    my $mTime = (stat $file)[9] or die appendLog("cannot find $file");
    my $diffTime = time() - $mTime;
    if ($diffTime >= $timeLimited) {
        return 1;
    }else{
        return 0;
    }
}

sub getOneRequestStatistic
{
		$request = $_;
		my $Reqform_xml = XMLin($request,forcearray => [ 'Register' ],KeyAttr=>[]);
			
		#filter trunk build request
		my $isTrunkBuilding     =  $Reqform_xml->{trunk_build};
		
		if($isTrunkBuilding eq 'true')
		{
			next;
		}
		my $req_time =  $Reqform_xml->{date};
		$req_time = filter_history_time($req_time);
		$req_time = filter_time_format($req_time);
		my $year = "";
		my $month = "";
		
		
		########################################################################################
		#			statistcs by month                                             #
		########################################################################################
		if($req_time =~ /(\d+)\/(\d+)\/(\d+) (.+)/ )
		{
			$year = $3;
			$month = $1;
		}
		else
		{
			$year = "before 2009 10";
			$month = " ";
		}
		
		my $halfYear = "Second half";
		if($month < 7)
		{
			$halfYear = "First half";
		}
		

		
		if(undef == $halfYearRef->{$halfYear." ".$year})
		{
			$halfYearRef->{$halfYear." ".$year} = {};
			$halfYearRef->{$halfYear." ".$year}->{'user'} = ();
		}
		
		if(undef ==  $yearRef->{$year} )
		{
			$yearRef->{$year} = {};
			$yearRef->{$year}->{'user'} = ();
		}
		
		if(undef ==  $monthRef->{$year." ".$month} )
		{
			$monthRef->{$year." ".$month} = {};
			$monthRef->{$year." ".$month}->{'user'} = ();
			$monthRef->{$year." ".$month}->{'reg'} = 0;
			$monthRef->{$year." ".$month}->{'oprom'} = 0;
			$monthRef->{$year." ".$month}->{'smu'} = 0;
			$monthRef->{$year." ".$month}->{'pmu'} = 0;
			$monthRef->{$year." ".$month}->{'psp'} = 0;
			$monthRef->{$year." ".$month}->{'cbs'} = 0;
			$monthRef->{$year." ".$month}->{'samu'} = 0;
		}
		
		my $SMU_Bin             = $Reqform_xml->{Processor}->{Platform}->{SMU};
		my $PMU_Bin             = $Reqform_xml->{Processor}->{Platform}->{PMU_INC};
		my $PSP_Bin             = $Reqform_xml->{Processor}->{Platform}->{PSP};
		my $Register_Modify     = $Reqform_xml->{Processor}->{Platform}->{Register};
		my $Oprom_Replace       = $Reqform_xml->{Processor}->{Platform}->{OPROM};
		my $CBS      		= $Reqform_xml->{Processor}->{Platform}->{CBS_Default};
		my $UCODE       	= $Reqform_xml->{Processor}->{Platform}->{UCODE};
		my $SAMU       	= $Reqform_xml->{Processor}->{Platform}->{SAMU};
		my $user		= $Reqform_xml->{requester};
		
		if(IsBVMTeamMember($user))
		{
			next;
		}
		
		push (@{$monthRef->{$year." ".$month}->{'user'}}, $user);
		push (@{$yearRef->{$year}->{'user'}}, $user);
		push (@{$halfYearRef->{$halfYear." ".$year}->{'user'}}, $user);
		
		if($Register_Modify)
		{
			$monthRef->{$year." ".$month}->{'reg'} ++;
			$total_reg ++;
		}
		if($Oprom_Replace)
		{
			$monthRef->{$year." ".$month}->{'oprom'} ++;
					$total_oprom ++;
		}
		if($SMU_Bin)
		{
			$monthRef->{$year." ".$month}->{'smu'} ++;
			$total_smu ++;
		}
		if($PMU_Bin)
		{
			$monthRef->{$year." ".$month}->{'pmu'} ++;
			$total_pmu ++;
		}
		if($PSP_Bin)
		{
			$monthRef->{$year." ".$month}->{'psp'} ++;
			$total_psp ++;
		}
		if($CBS)
		{
			$monthRef->{$year." ".$month}->{'cbs'} ++;
			$total_cbs ++;
		}
		if($UCODE)
		{
			$monthRef->{$year." ".$month}->{'ucode'} ++;
			$total_ucode ++;
		}
		if($SAMU)
		{
			$monthRef->{$year." ".$month}->{'samu'} ++;
			$total_samu ++;
		}
		########################################################################################
		#			statistcs by user                                              #
		########################################################################################

		if(undef ==  $userReference->{$user} )
		{
			$userReference->{$user}->{'platform'} = ();
			$userReference->{$user}->{'reg'} = 0;
			$userReference->{$user}->{'oprom'} = 0;
			$userReference->{$user}->{'smu'} = 0;
			$userReference->{$user}->{'pmu'} = 0;
			$userReference->{$user}->{'psp'} = 0;
			$userReference->{$user}->{'cbs'} = 0;
			$userReference->{$user}->{'samu'} = 0;
		}
		
		push (@{$userReference->{$user}->{'platform'}}, $Reqform_xml->{Processor}->{Platform}->{name});
		if($Register_Modify)
		{
			$userReference->{$user}->{'reg'} ++;
		}
		if($Oprom_Replace)
		{
			$userReference->{$user}->{'oprom'} ++;
		}
		if($SMU_Bin)
		{
			$userReference->{$user}->{'smu'} ++;
		}
		if($PMU_Bin)
		{
			$userReference->{$user}->{'pmu'} ++;
		}
		if($PSP_Bin)
		{
			$userReference->{$user}->{'psp'} ++;
		}
		if($CBS)
		{
			$userReference->{$user}->{'cbs'} ++;
		}
		if($UCODE)
		{
			$userReference->{$user}->{'ucode'} ++;
		}
		if($SAMU)
		{
			$userReference->{$user}->{'samu'} ++;
		}
		########################################################################################
		#			statistcs by platform                                          #
		########################################################################################
		my $platform = $Reqform_xml->{Processor}->{Platform}->{name};
		
		if(undef ==  $platformReference->{$platform} )
		{
			$platformReference->{$platform}->{'user'} = ();
			$platformReference->{$platform}->{'reg'} = 0;
			$platformReference->{$platform}->{'oprom'} = 0;
			$platformReference->{$platform}->{'smu'} = 0;
			$platformReference->{$platform}->{'pmu'} = 0;
			$platformReference->{$platform}->{'psp'} = 0;
			$platformReference->{$platform}->{'cbs'} = 0;
			$platformReference->{$platform}->{'ucode'} = 0;
			$platformReference->{$platform}->{'samu'} = 0;
		}
		
		push (@{$platformReference->{$platform}->{'user'}}, $user);
		if($Register_Modify)
		{
			$platformReference->{$platform}->{'reg'} ++;
		}
		if($Oprom_Replace)
		{
			$platformReference->{$platform}->{'oprom'} ++;
		}
		if($SMU_Bin)
		{
			$platformReference->{$platform}->{'smu'} ++;
		}
		if($PMU_Bin)
		{
			$platformReference->{$platform}->{'pmu'} ++;
		}
		if($PSP_Bin)
		{
			$platformReference->{$platform}->{'psp'} ++;
		}
		if($CBS)
		{
			$platformReference->{$platform}->{'cbs'} ++;
		}
		if($UCODE)
		{
			$platformReference->{$platform}->{'ucode'} ++;
		}
		if($SAMU)
		{
			$platformReference->{$platform}->{'samu'} ++;
		}

		$summaryStatic{"total_reg"} = $total_reg;
		$summaryStatic{"total_oprom"} = $total_oprom;
		$summaryStatic{"total_smu"} = $total_smu;
		$summaryStatic{"total_pmu"} = $total_pmu;
		$summaryStatic{"total_psp"} = $total_psp;
		$summaryStatic{"total_cbs"} = $total_cbs;
		$summaryStatic{"total_ucode"} = $total_ucode;
		$summaryStatic{"total_samu"} = $total_samu;		
}