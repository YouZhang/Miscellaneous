#! perl -w
use strict;
use File::Find;
use File::Copy;

#-----------global var------------------------#
my %cleanPath = (
    "Temp" => 'C:\Temp',
    "REPO" => 'F:\bvm\REPO',
    "UserBIOS" => 'F:\bvm\BDB\UserBIOS',
    "BVMBIOS" => 'F:\bvm\BDB\BVMBIOS'                 
);


my $today = getDate();
my $log= 'F:\clean-guide\cleanLog.txt';
my $monthInSec = 3600 * 24 * 30;
my $weekInSec = 3600 * 24 * 7;
#for debug
#my $monthInSec = 1000;

my $backupDir = "G:\\BVM_BIN_BACK_UP_$today";


Main();
sub Main{
    appendLog("#---------$today Temp cleaning Start-------------#");
    delTemp();
    appendLog("#---------$today Temp cleaning End-------------#");
    #------------------------------------------------------------------------
    appendLog("#---------$today REPO cleaning Start-------------#");
    delREPO();
    appendLog("#---------$today REPO cleaning end-------------#");
    #------------------------------------------------------------------------
    appendLog("#---------$today UserBIOS cleaning Start-------------#");
    delUserBIOS();
    appendLog("#---------$today UserBIOS cleaning End-------------#");
    #------------------------------------------------------------------------
    appendLog("#---------$today BVMBIOS cleaning Start-------------#");
    del_BakBVMBIOS();
    appendLog("#---------$today BVMBIOS cleaning End-------------#");
}


#----------------------Methods--------------------------#
sub delTemp{
    my $cleanPath = $cleanPath{"Temp"};
    my $index;
    my $file;
    chdir $cleanPath;
    opendir(DIRHANDLE,$cleanPath) or die appendLog("cannot open $cleanPath");
    my @files = readdir(DIRHANDLE);
    closedir(DIRHANDLE);
    #delete expect the . or ..;
    for($index = 2;$index < scalar @files; $index++){
        $file = $files[$index];
        if ( $file ne "OVO-Agent" ) {
            delFile($file);
            appendLog("Successfully delete $file");
        }
    }
}

sub delREPO{
    my $cleanPath = $cleanPath{"REPO"};
    my $index;
    my $file;
    chdir $cleanPath;
    my @files = getFilesInDir($cleanPath);
    #delete expect the . or ..;
    for($index = 2;$index < scalar @files; $index++){
        $file = $files[$index];
        if ( isOldFile($file,$monthInSec) ) {
            delFile($file);
            appendLog("Successfully delete $file");
        }
    }    
}

sub delUserBIOS{
    my $cleanPath = $cleanPath{"UserBIOS"};
    my $index;
    my $file;
    chdir $cleanPath;
    my @files = getFilesInDir($cleanPath);
    #delete expect the . or ..;
    for($index = 2;$index < scalar @files; $index++){
        $file = $files[$index];
        if ( isOldFile($file,$monthInSec) ) {
            delFile($file);
            appendLog("Successfully delete $file");
        }
    }
}

sub del_BakBVMBIOS{
    my $cleanPath = $cleanPath{"BVMBIOS"};
    my $index;
    my $file;
    my $fileFolder;
    if (!-d $backupDir) {
        mkdir($backupDir) or die appendLog("make directory failed!");
    }
    if (!-d $backupDir) {
        mkdir($backupDir) or die appendLog("make directory failed!");
    }   
    find(\&wanted,$cleanPath);
    chdir $cleanPath;
    my @files = getFilesInDir($cleanPath);
    #delete expect the . or ..;
    for($index = 2;$index < scalar @files; $index++){
        
        $file = $files[$index];
        $fileFolder = $backupDir."\\".$file;
        if (!-d $fileFolder) {
            mkdir($fileFolder) or die appendLog("make directory failed!");
        }
        if ( isOldFile($file,$monthInSec) ) {
            system("xcopy $file $fileFolder");
            appendLog("Successfully move $cleanPath\\$file to $fileFolder");
            delFile($file);
        }
    }
}


sub getFilesInDir{
    my $path = shift;
    opendir(DIRHANDLE,$path) or die appendLog("cannot open $path");
    my @files = readdir(DIRHANDLE);
    closedir(DIRHANDLE);
    return @files;
}


sub wanted{
    my $curFile = $_;  #$_ current file name without path;
    #my $curPath = $File::Find::dir;
    if (-d $curFile and $curFile =~ /temp/ and isOldFile($curFile,$weekInSec)) {
        delFile($curFile);
        appendLog("successfully delete temp folder in $curFile");
    }
}


sub isOldFile{
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


sub delFile{
    my $file = shift; 
    if (-d $file) {
        system("rd /s /q $file");		
    }else{
        unlink($file) or die appendLog("delete file $file failed!\n");   
    }
}


sub getDate{
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
    $year += 1900;
    $mon++;
    my $date = sprintf("%04d-%02d-%02d", $year, $mon, $mday);
    return $date;
}


sub appendLog{
    
    my $text = shift;
    open (LOG_FILE, ">>",$log) or print "Cannot open $log for write.";
    print LOG_FILE $text."\n\n";
    print $text."\n";
    close LOG_FILE;
}




#----------------------------------------#

#test_All();

#------------------
sub test_All{
    test_fileTimeDiff();
    #delTemp();
    #delREPO();
    #delUserBIOS();
    del_BakBVMBIOS();
}

sub test_delTemp{
    delTemp();  
}

sub test_fileTimeDiff{
    print isOldFile('C:\Temp\CGItemp55281',$monthInSec);
}
