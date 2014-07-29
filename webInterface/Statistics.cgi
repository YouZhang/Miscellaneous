#!c:/Perl/bin/perl.exe

# includes
use CGI qw/-tabindex -nosticky :all/;
use POSIX qw(ceil floor);
use Fcntl qw(:flock);
use File::Copy;
use DBI; # Database support; needed for MySQL.
use Array::Unique;
use Cwd;
use XML::Simple;
use Time::Local;
use Sys::Hostname;
use bigint;
use Storable;

require('F:\bvm\CGI\Common.pl');
my $cgi_dir	= getcwd();
my $bvm_root_dir = $cgi_dir;
while($bvm_root_dir =~ s/\//\\/i){};
$bvm_root_dir =~ s/\\cgi$//i;

my $user_bios_bin = '';
# Header info for the pages
my $bgcolor = "white";
my $bgtable = "white";
my $fontcolor = "black";
my $linkcolor = "blue";
my $cellcolor_light = "#FFFFFF";
my $cellcolor_dark = "#EFEFEF";
my $title = 'BIOS Vending Machine';
my $table_size = "90%";
my $estimated_build_time = 6;

# Defines the current working directory and config file path
my $cwd = "${cgi_dir}\\";
my $config_file = "${bvm_root_dir}\\sys_cfg.xml";
my $confighash = XMLin($config_file, forcearray => 1);
my $link_hash = XMLin($config_file, keyAttr =>[],forcearray => [ 'LINK' ]);
my $hostname = hostname();
my $downloadURL = 'http://'.$hostname.'/BVMBIOS';

my $platformStatistics = "F:\\clean-guide\\monthStatistics.txt";
my $monthStatistics = "F:\\clean-guide\\PlatformStatistics.txt";
my $yearStatistics = "F:\\clean-guide\\YearStatistics.txt";
my $halfYearStatistics = "F:\\clean-guide\\HalfYearStatistics.txt";
my $userStatistics = "F:\\clean-guide\\UserStatistics.txt";
my $summaryStatistics = "F:\\clean-guide\\SummaryStatistics.txt";



my $is_file_bvm_support = '';
# Path for the log file
my $loghash = ();

my @g_BVM_TEAM = ('David.Ju@amd.com', 'Bob.Yang@amd.com', 'Roger.Gu@amd.com','Renbo.Jiang@amd.com','You.Zhang@amd.com');

print_view_history();

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

sub print_view_history
{
	my $bdb_dir = "${bvm_root_dir}\\BDB";
	my $req_dir = "${bvm_root_dir}\\BDB\\REQFORM";
	my $cellcolor_count = 0;
	my $cellcolor = "";

    # Prints the web page header
    print header,start_html( -title=>$title, -author=>$link_hash->{webmaster}, -bgcolor=>$bgcolor,
                    -link=>$linkcolor, -alink=>$linkcolor, -vlink=>$linkcolor,
                    -style=>{-src=>"css/bvmstyle.css"},
                    -script=>[{-src=>"js/bvmscript.js", -type=>"text/javascript"},
                          {-src=>"js/sorttable.js", -type=>"text/javascript"}]
                    ), "\n",
                    "\n", p, "\n";
    print start_form;

	chdir $req_dir;
	my @requests_list = glob "*.xml";
	@requests_list = sort {$b cmp $a} @requests_list;

  	if (scalar(@requests_list) != 0)
	{
        my $yearStatic = retrieve($yearStatistics);
        my $halfYearStatic = retrieve($halfYearStatistics);
        my $monthStatic = retrieve($monthStatistics);
        my $userStatic = retrieve($userStatistics);
        my $platformStatic = retrieve($platformStatistics);
		my $summaryStatic = retrieve($summaryStatistics);

        my $total_cbs = 0;
        my $total_reg = 0;
		my $total_oprom = 0;
        my $total_smu = 0;
        my $total_pmu = 0;
        my $total_psp = 0;
        my $total_ucode = 0;
		my $total_samu = 0;

	    foreach (@requests_list)
	    {
            $read = $_;
            my $Reqform_xml    = XMLin($read,forcearray => [ 'Register' ],KeyAttr=>[]);

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

            #######################################################################################


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

            if(undef == $halfYearStatic->{$halfYear." ".$year})
            {
            	$halfYearStatic->{$halfYear." ".$year} = {};
                $halfYearStatic->{$halfYear." ".$year}->{'user'} = ();
            }

            if(undef ==  $yearStatic->{$year} )
            {
            	$yearStatic->{$year} = {};
                $yearStatic->{$year}->{'user'} = ();
            }

            if(undef ==  $monthStatic->{$year." ".$month} )
            {
            	$monthStatic->{$year." ".$month} = {};
                $monthStatic->{$year." ".$month}->{'user'} = ();
                $monthStatic->{$year." ".$month}->{'reg'} = 0;
                $monthStatic->{$year." ".$month}->{'oprom'} = 0;
                $monthStatic->{$year." ".$month}->{'smu'} = 0;
                $monthStatic->{$year." ".$month}->{'pmu'} = 0;
                $monthStatic->{$year." ".$month}->{'psp'} = 0;
                $monthStatic->{$year." ".$month}->{'cbs'} = 0;
				$monthStatic->{$year." ".$month}->{'samu'} = 0;
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

            push (@{$monthStatic->{$year." ".$month}->{'user'}}, $user);
            push (@{$yearStatic->{$year}->{'user'}}, $user);
            push (@{$halfYearStatic->{$halfYear." ".$year}->{'user'}}, $user);

            if($Register_Modify)
            {
            	$monthStatic->{$year." ".$month}->{'reg'} ++;
        		$total_reg ++;
            }
            if($Oprom_Replace)
            {
            	$monthStatic->{$year." ".$month}->{'oprom'} ++;
				$total_oprom ++;
            }
            if($SMU_Bin)
            {
            	$monthStatic->{$year." ".$month}->{'smu'} ++;
        		$total_smu ++;
            }
            if($PMU_Bin)
            {
            	$monthStatic->{$year." ".$month}->{'pmu'} ++;
        		$total_pmu ++;
            }
            if($PSP_Bin)
            {
            	$monthStatic->{$year." ".$month}->{'psp'} ++;
        		$total_psp ++;
            }
            if($CBS)
            {
            	$monthStatic->{$year." ".$month}->{'cbs'} ++;
                $total_cbs ++;
            }
            if($UCODE)
            {
                $monthStatic->{$year." ".$month}->{'ucode'} ++;
                $total_ucode ++;
            }
			if($SAMU)
			{
				$monthStatic->{$year." ".$month}->{'samu'} ++;
                $total_samu ++;
			}
            ########################################################################################
            #			statistcs by user                                              #
            ########################################################################################
            if(undef ==  $userStatic->{$user} )
            {
            	$userStatic->{$user}->{'platform'} = ();
                $userStatic->{$user}->{'reg'} = 0;
                $userStatic->{$user}->{'oprom'} = 0;
                $userStatic->{$user}->{'smu'} = 0;
                $userStatic->{$user}->{'pmu'} = 0;
                $userStatic->{$user}->{'psp'} = 0;
                $userStatic->{$user}->{'cbs'} = 0;
				$userStatic->{$user}->{'samu'} = 0;
            }

            push (@{$userStatic->{$user}->{'platform'}}, $Reqform_xml->{Processor}->{Platform}->{name});
            if($Register_Modify)
            {
            	$userStatic->{$user}->{'reg'} ++;
            }
            if($Oprom_Replace)
            {
            	$userStatic->{$user}->{'oprom'} ++;
            }
            if($SMU_Bin)
            {
            	$userStatic->{$user}->{'smu'} ++;
            }
            if($PMU_Bin)
            {
            	$userStatic->{$user}->{'pmu'} ++;
            }
            if($PSP_Bin)
            {
            	$userStatic->{$user}->{'psp'} ++;
            }
            if($CBS)
            {
            	$userStatic->{$user}->{'cbs'} ++;
            }
            if($UCODE)
            {
                $userStatic->{$user}->{'ucode'} ++;
            }
			if($SAMU)
            {
                $userStatic->{$user}->{'samu'} ++;
            }
            ########################################################################################
            #			statistcs by platform                                          #
            ########################################################################################
            my $platform = $Reqform_xml->{Processor}->{Platform}->{name};
            if(undef ==  $platformStatic->{$platform} )
            {
            	$platformStatic->{$platform}->{'user'} = ();
                $platformStatic->{$platform}->{'reg'} = 0;
                $platformStatic->{$platform}->{'oprom'} = 0;
                $platformStatic->{$platform}->{'smu'} = 0;
                $platformStatic->{$platform}->{'pmu'} = 0;
                $platformStatic->{$platform}->{'psp'} = 0;
                $platformStatic->{$platform}->{'cbs'} = 0;
                $platformStatic->{$platform}->{'ucode'} = 0;
				$platformStatic->{$platform}->{'samu'} = 0;
            }

            push (@{$platformStatic->{$platform}->{'user'}}, $user);
            if($Register_Modify)
            {
            	$platformStatic->{$platform}->{'reg'} ++;
            }
            if($Oprom_Replace)
            {
            	$platformStatic->{$platform}->{'oprom'} ++;
            }
            if($SMU_Bin)
            {
            	$platformStatic->{$platform}->{'smu'} ++;
            }
            if($PMU_Bin)
            {
            	$platformStatic->{$platform}->{'pmu'} ++;
            }
            if($PSP_Bin)
            {
            	$platformStatic->{$platform}->{'psp'} ++;
            }
            if($CBS)
            {
            	$platformStatic->{$platform}->{'cbs'} ++;
            }
            if($UCODE)
            {
            	$platformStatic->{$platform}->{'ucode'} ++;
            }
			if($SAMU)
            {
            	$platformStatic->{$platform}->{'samu'} ++;
            }
	    }

        ###############################################################################################

        ########################################################################################
        #			print by month		                                           #
        ########################################################################################
        print "<br><br>";
        print "<center><H1>Statistics by month</H1></center>";
        print "<table width=$table_size border='2' align='center' class = 'tb tb2 sortable'>\n";
        print "
            <tr>
            <th style=\"cursor:hand\">Month</th>
            <th style=\"cursor:hand\">Users</th>
            <th style=\"cursor:hand\">Register Modification</th>
            <th style=\"cursor:hand\">Option Rom Replacement</th>
            <th style=\"cursor:hand\">SMU Header Replacement</th>
            <th style=\"cursor:hand\">PMU Replacement</th>
            <th style=\"cursor:hand\">PSP Entry Replacement</th>
            <th style=\"cursor:hand\">CBS Default Modification</th>
            <th style=\"cursor:hand\">Micro Code Update</th>
			<th style=\"cursor:hand\">SAMU Binary Replacement</th>
            <th style=\"cursor:hand\">Total</th>
            </tr>";
        my $cellcolor_count = 0;
        my $cellcolor = $cellcolor_light;
        foreach $key (sort keys %{$monthStatic})
        {
        	$value =$monthStatic -> {$key};
            if($value == undef)
            {
            	next;
            }
            $cellcolor_count++;
            if (($cellcolor_count%2)==0) {
                $cellcolor = $cellcolor_dark;
            }
            else {
                $cellcolor = $cellcolor_light;
            }

            print   "<tr bgcolor='$cellcolor' valign='top' align='left'>";
            print   "<td align='center' width = '100'>$key</td>";
            {
            	print   "<td align='center' width = '200'>";
                my @users = @{$value->{'user'}};
                ##################################
        		my %saw;
        		my @users=grep(!$saw{$_}++,@users);
                ##################################
                for(my $i = 0; $i < @users; $i ++ )
                {
                	print   $users[$i];
                        print "<br>";
                }
                print "</td>";
            }
            print   "<td align='center' width = '100'>".$value->{'reg'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'oprom'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'smu'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'pmu'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'psp'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'cbs'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'ucode'}."</td>";
			print   "<td align='center' width = '100'>".$value->{'samu'}."</td>";
            print   "<td align='center' width = '100'>".($value->{'reg'} + $value->{'oprom'} + $value->{'smu'} + $value->{'pmu'} + $value->{'psp'}+ $value->{'cbs'} + $value->{'ucode'} + $value->{'samu'})."</td>";
        	print   "</tr>";
        }
	    print "</table>\n";

        ########################################################################################
        #			print by user		                                           #
        ########################################################################################
        print "<br><br>";
        print "<center><H1>Statistics by user</H1></center>";
        print "<table width=$table_size border='2' align='center' class = 'tb tb2 sortable'>\n";
        print "
            <tr>
            <th  width = '100' style=\"cursor:hand\">User</th>
            <th  width = '200' style=\"cursor:hand\">Platforms</th>
            <th  width = '100' style=\"cursor:hand\">Register Modification</th>
            <th  width = '100' style=\"cursor:hand\">Option Rom Replacement</th>
            <th  width = '100' style=\"cursor:hand\">SMU Header Replacement</th>
            <th  width = '100' style=\"cursor:hand\">PMU Replacement</th>
            <th  width = '100' style=\"cursor:hand\">PSP Directory Entry Replacement</th>
            <th  width = '100' style=\"cursor:hand\">CBS Default Modification</th>
            <th  width = '100' style=\"cursor:hand\">Micro Code Update</th>
			<th  width = '100' style=\"cursor:hand\">SAMU Binary Replacement</th>
            <th  width = '100'style=\"cursor:hand\">Total</th>
            </tr>";
        my $cellcolor_count = 0;
        my $cellcolor = $cellcolor_light;
        while(my ($key, $value) = each (%{$userStatic}))
        {
            if($value == undef)
            {
            	next;
            }
            $cellcolor_count++;
            if (($cellcolor_count%2)==0) {
                    $cellcolor = $cellcolor_dark;
            }
            else {
                    $cellcolor = $cellcolor_light;
            }

            print   "<tr bgcolor='$cellcolor' valign='top' align='left'>";
            print   "<td align='center' width = '100'>$key</td>";
            {
            	print   "<td align='center' width = '200'>";
                my @users = @{$value->{'platform'}};
                ##################################
		        my %saw;
		        my @users=grep(!$saw{$_}++,@users);
                ##################################
                for(my $i = 0; $i < @users; $i ++ )
                {
                	print   $users[$i];
                    print "<br>";
                }
                print "</td>";
            }
            print   "<td align='center' width = '100'>".$value->{'reg'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'oprom'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'smu'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'pmu'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'psp'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'cbs'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'ucode'}."</td>";
			print   "<td align='center' width = '100'>".$value->{'samu'}."</td>";
            print   "<td align='center' width = '100'>".($value->{'reg'} + $value->{'oprom'} + $value->{'smu'} + $value->{'pmu'} + $value->{'psp'}  +$value->{'cbs'} + $value->{'ucode'} + $value->{'samu'})."</td>";
        	print   "</tr>";
        }
	    print "</table>\n";

        ########################################################################################
        #			print by platform                                                 #
        ########################################################################################
        print "<br><br>";
        print "<center><H1>Statistics by platform</H1></center>";
        print "<table width=$table_size border='2' align='center' class = 'tb tb2 sortable'>\n";
        print "
            <tr>
            <th style=\"cursor:hand\">Platform</th>
            <th style=\"cursor:hand\">Users</th>
            <th style=\"cursor:hand\">Register Modification</th>
            <th style=\"cursor:hand\">Option Rom Replacement</th>
            <th style=\"cursor:hand\">SMU Header Replacement</th>
            <th style=\"cursor:hand\">PMU Replacement</th>
            <th style=\"cursor:hand\">PSP Directory Entry Replacement</th>
            <th style=\"cursor:hand\">CBS Default Modification</th>
            <th style=\"cursor:hand\">Micro Code Update</th>
			<th style=\"cursor:hand\">SAMU Binary Replacement</tj>
            <th style=\"cursor:hand\">Total</th>
            </tr>";
        my $cellcolor_count = 0;
        my $cellcolor = $cellcolor_light;
        while(my ($key, $value) = each (%{$platformStatic}))
        {
            if($value == undef)
            {
            	next;
            }
            $cellcolor_count++;
            if (($cellcolor_count%2)==0) {
                $cellcolor = $cellcolor_dark;
            }
            else {
                $cellcolor = $cellcolor_light;
            }

            print   "<tr bgcolor='$cellcolor' valign='top' align='left'>";
            print   "<td align='center' width = '100'>$key</td>";
            {
            	print   "<td align='center' width = '200'>";
                my @users = @{$value->{'user'}};
                ##################################
        		my %saw;
        		my @users=grep(!$saw{$_}++,@users);
                ##################################
                for(my $i = 0; $i < @users; $i ++ )
                {
                	print   $users[$i];
                    print "<br>";
                }
                print "</td>";
            }
            print   "<td align='center' width = '100'>".$value->{'reg'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'oprom'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'smu'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'pmu'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'psp'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'cbs'}."</td>";
            print   "<td align='center' width = '100'>".$value->{'ucode'}."</td>";
			print   "<td align='center' width = '100'>".$value->{'samu'}."</td>";
            print   "<td align='center' width = '100'>".($value->{'reg'} + $value->{'oprom'} + $value->{'smu'} + $value->{'pmu'} + $value->{'psp'} +$value->{'cbs'} + $value->{'ucode'} + $value->{'samu'})."</td>";
        	print   "</tr>";
        }
	    print "</table>\n";

        print "<center><H1>Summary</H1></center>";
        print "<table width=$table_size border='2' align='center' class = 'tb tb2 sortable'>\n";
        print "
            <tr>
            <th style=\"cursor:hand\">Register Modification</th>
            <th style=\"cursor:hand\">Option Rom Replacement</th>
            <th style=\"cursor:hand\">SMU Header Replacement</th>
            <th style=\"cursor:hand\">PMU Replacement</th>
            <th style=\"cursor:hand\">PSP Directory Entry Replacement</th>
            <th style=\"cursor:hand\">CBS Default Modification</th>
            <th style=\"cursor:hand\">Micro Code Update</th>
			<th style=\"cursor:hand\">SAMU Binary Replacement</th>
            <th style=\"cursor:hand\">Total</th>
            </tr>";
		foreach $key (sort keys %{$summaryStatistics})
        {
        	$value = $monthStatic -> {$key};
			$total = $total + $value;
		}
        $total = $total + $total_reg +  $total_oprom +  $total_smu + $total_pmu + $total_psp + $total_cbs + $total_ucode +$total_samu;
        print "
            <tr>
            <td> $total_reg</td>
            <td> $total_oprom</td>
            <td> $total_smu</td>
            <td> $total_pmu</td>
            <td> $total_psp</td>
            <td> $total_cbs</td>
            <td> $total_ucode</td>
			<td> $total_samu</td>
            <td> $total</td>
            </tr>";
        print "</table><br>\n";

        ################################################################
        print "<br><br>";
        print "<center><H1>Statistics by year</H1></center>";
        print "<table width=$table_size border='2' align='center' class = 'tb tb2 sortable'>\n";
        print "
            <tr>
            <th style=\"cursor:hand\">Year</th>
            <th style=\"cursor:hand\">Users</th>
            <th style=\"cursor:hand\">Request</th>
            </tr>";
        my $cellcolor_count = 0;
        my $cellcolor = $cellcolor_light;
        foreach $key (sort keys %{$yearStatic})
        {
        	$value =$yearStatic -> {$key};
            if($value == undef)
            {
            	next;
            }
            $cellcolor_count++;
            if (($cellcolor_count%2)==0) {
                    $cellcolor = $cellcolor_dark;
            }
            else {
                    $cellcolor = $cellcolor_light;
            }

            print   "<tr bgcolor='$cellcolor' valign='top' align='left'>";
            my $request_count = 0;
            print   "<td align='center' width = '100'>$key</td>";
            {
            	print   "<td align='center' width = '200'>";
                my @users = @{$value->{'user'}};
                $request_count = @users;
                ##################################
        		my %saw;
        		my @users=grep(!$saw{$_}++,@users);
                ##################################
                for(my $i = 0; $i < @users; $i ++ )
                {
                	print   $users[$i];
                    print "<br>";
                }
                my $user_count = @users;
                print "<br> user number: ".@users;
                print "</td>";
            }
            print   "<td align='center' width = '100'>".$request_count."</td>";
            print   "</tr>";
        }
	    print "</table>\n";
        ################################################################
        print "<br><br>";
        print "<center><H1>Statistics by half year</H1></center>";
        print "<table width=$table_size border='2' align='center' class = 'tb tb2 sortable'>\n";
        print " <tr>
	            <th style=\"cursor:hand\">Year</th>
	            <th style=\"cursor:hand\">Users</th>
	            <th style=\"cursor:hand\">Request</th>
	            </tr>";
        my $cellcolor_count = 0;
        my $cellcolor = $cellcolor_light;
        foreach $key (sort keys %{$halfYearStatic})
        {
        	$value =$halfYearStatic -> {$key};
            if($value == undef)
            {
            	next;
            }
            $cellcolor_count++;
            if (($cellcolor_count%2)==0) {
                    $cellcolor = $cellcolor_dark;
            }
            else {
                    $cellcolor = $cellcolor_light;
            }

            print   "<tr bgcolor='$cellcolor' valign='top' align='left'>";
            my $request_count = 0;
            print   "<td align='center' width = '100'>$key</td>";
            {
            	print   "<td align='center' width = '200'>";
                my @users = @{$value->{'user'}};
                $request_count = @users;
                ##################################
        		my %saw;
        		my @users=grep(!$saw{$_}++,@users);
                ##################################
                for(my $i = 0; $i < @users; $i ++ )
                {
                	print   $users[$i];
                    print "<br>";
                }
                my $user_count = @users;
                print "<br> user number: ".@users;
                print "</td>";
            }
            print   "<td align='center' width = '100'>".$request_count."</td>";
            print   "</tr>";
        }
	    print "</table>\n";
        ################################################################

	  } # end if
	  else {
	    print "<tr><td>No builds found</td><tr>\n";
	    print "</table>";
	  } # end else

    print end_form;
	print end_html;
} # end sub