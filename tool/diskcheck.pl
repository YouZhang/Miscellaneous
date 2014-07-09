use strict;

my $cwd = 'F:\bvm\EXE';
my $webmaster = 'Renbo.Jiang@amd.com;You.Zhang@amd.com';
my $attachedLogFile = 'F:\clean-guide\cleanLog.txt';

main(); 

sub getDiskStatus
{
    my $disk = shift;
    my $command = "wmic LogicalDisk where \"Caption='";
    $command .= $disk;
    $command .= "'\" get FreeSpace,Size /value ";  
    
    my @output = readpipe($command);
    my $result = $disk." free space is: ";
    foreach(@output)
    {
        #FreeSpace=10487459840
        if( $_ =~ /\s*FreeSpace\s*=\s*(\d+)\s*/ )
        {
            my $size = $1;
            $size = $size/1024;
            $size = $size/1024; 
            $result .= $size;
            $result .= "M";             
        }     
    }
    print "\n$result";
    return $result;
}

sub sendMail
{
    my $message = shift;
    my $Email_command = "\"${cwd}\\sendemail.exe\"  -s aussmtp.amd.com -f BVM_SYSTEM_SERVICE\@amd.com";
 
	$Email_command .= " -t $webmaster";
	$Email_command .= " -u \"BIOS Vending Machine: Server Disk Check\" ";
	my $failed;
	#attched log file
	$Email_command .= " -a \"".$attachedLogFile."\"";
	# email body
	$Email_command .= " -m \"".$message."\""; 
 
	# Calls the e-mail script
	print "\n$Email_command"; 
	`$Email_command`;   
	print "\nmail sent!"; 
}

sub main{ 
    my $message = "Below is the disk status:\\n";
    $message .= "\t";
    $message .= getDiskStatus("C:");
    
    $message .= "\\n\t";
    $message .= getDiskStatus("F:");
    
    sendMail($message); 
}
