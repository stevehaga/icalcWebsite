#!/usr/bin/perl
##############################################################################
# Friends postcard script             Version 1                                #
# COPYRIGHT NOTICE                                                           #
# Copyright 1998 Chris Tong, Enchanted Websites. All Rights Reserved.                                                                                           
#                                                                            #
# Obtain permission before redistributing this software over the Internet or #
# in any other medium.	In all cases copyright and header must remain
# intact.
##############################################################################
# Set Variables

$dbfile = "../database/friends.db";
$date_command = "/bin/date";

# Set Your Options:
$uselog = 1;            # 1 = Yes; 0 = No
$linkmail = 1;          # 1 = Yes; 0 = No
$separator = 1;         # 1 = <hr>; 0 = <p>
$redirection = 0;       # 1 = Yes; 0 = No
$entry_order = 1;       # 1 = Newest entries added first;
                        # 0 = Newest Entries added last.
$allow_html = 1;        # 1 = Yes; 0 = No
$line_breaks = 1;	# 1 = Yes; 0 = No

$mailprog = '/bin/sendmail';		## was /usr/lib/sendmail

# Done
##############################################################################

# Get the Date for Entry
$date = `$date_command +"%A, %B %d, %Y at %T (%Z)"`; chop($date);
$shortdate = `$date_command +"%D %T %Z"`; chop($shortdate);
$day = `$date_command +"%D"`; 
chop($day);
$time = `$date_command +"%T"`; 
chop($time);
$zone = `$date_command +"%Z"`; 
chop($zone);

# Get the input
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});

# Split the name-value pairs
@pairs = split(/&/, $buffer);

foreach $pair (@pairs) {
   ($name, $value) = split(/=/, $pair);

   # Un-Webify plus signs and %-encoding
   $value =~ tr/+/ /;
   $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
   $value =~ s/<!--(.|\n)*-->//g;

   if ($allow_html != 1) {
      $value =~ s/<([^>]|\n)*>//g;
   }

   $FORM{$name} = $value;
}

# inputs: name, email, message

$fname=$FORM{'fname'};		## sender info
$lname=$FORM{'lname'};
$email=$FORM{'email'};
$messageq=$FORM{'messageq'};

$fname1=$FORM{'fname1'};	## recipient info
$lname1=$FORM{'lname1'};
$email1=$FORM{'email1'};
$message1=$FORM{'message1'};
$fname2=$FORM{'fname2'};
$lname2=$FORM{'lname2'};
$email2=$FORM{'email2'};
$message2=$FORM{'message2'};
$fname3=$FORM{'fname3'};
$lname3=$FORM{'lname3'};
$email3=$FORM{'email3'};
$message3=$FORM{'message3'};
$fname4=$FORM{'fname4'};
$lname4=$FORM{'lname4'};
$email4=$FORM{'email4'};
$message4=$FORM{'message4'};
$fname5=$FORM{'fname5'};
$lname5=$FORM{'lname5'};
$email5=$FORM{'email5'};
$message5=$FORM{'message5'};
$fname6=$FORM{'fname6'};
$lname6=$FORM{'lname6'};
$email6=$FORM{'email6'};
$message6=$FORM{'message6'};
$fname7=$FORM{'fname7'};
$lname7=$FORM{'lname7'};
$email7=$FORM{'email7'};
$message7=$FORM{'message7'};
$fname8=$FORM{'fname8'};
$lname8=$FORM{'lname8'};
$email8=$FORM{'email8'};
$message8=$FORM{'message8'};
$fname9=$FORM{'fname9'};
$lname9=$FORM{'lname9'};
$email9=$FORM{'email9'};
$message9=$FORM{'message9'};
$fname10=$FORM{'fname10'};
$lname10=$FORM{'lname10'};
$email10=$FORM{'email10'};
$message10=$FORM{'message10'};

# No blank checking. Simply ignore entries
# that are incomplete.


# Remove carriage returns from TEXTAREAs.

$message1 =~ s/\n//g;
$message2 =~ s/\n//g; 
$message3 =~ s/\n//g; 
$message4 =~ s/\n//g; 
$message5 =~ s/\n//g; 
$message6 =~ s/\n//g; 
$message7 =~ s/\n//g; 
$message8 =~ s/\n//g; 
$message9 =~ s/\n//g; 
$message10 =~ s/\n//g;  

 # Print Beginning of Acknowledgement Page

   print "Content-Type: text/html\n\n";
   print "<html><head><title>Your postcards have been sent!</title></head>\n";
   print "<BODY TEXT=\"#000080\" BGCOLOR=\"#FFFFFF\" LINK=\"#0000EE\" 
VLINK=\"#FF0000\" ALINK=\"#0080FF\"><font face=\"arial,helvetica\">\n";

   # Print Response

   print "<center><img src=\"../title_w_new1_sm.jpg\" width=285 height=76 alt=\"QuickCalc\"><br><b><font size=+1><font color=\"FF0000\">P</font>ostcards <font color=\"FF0000\">S</font>ent!</font></b><img src=\"stamp1.jpg\" width=75 height=75 hspace=10 align=middle></center><br><br>\n";
   print "<center><table width=80%><tr><td>\n";
   print "<font face=\"arial\"><b>We have sent your postcards to\n";
   print "the following friends:</b><br><br><hr>\n";

# Update the prospect database and email the recipient

&updateDBandMail($fname1, $lname1, $email1, $message1);
&updateDBandMail($fname2, $lname2, $email2, $message2);
&updateDBandMail($fname3, $lname3, $email3, $message3);
&updateDBandMail($fname4, $lname4, $email4, $message4);
&updateDBandMail($fname5, $lname5, $email5, $message5);
&updateDBandMail($fname6, $lname6, $email6, $message6);
&updateDBandMail($fname7, $lname7, $email7, $message7);
&updateDBandMail($fname8, $lname8, $email8, $message8);
&updateDBandMail($fname9, $lname9, $email9, $message9);
&updateDBandMail($fname10, $lname10, $email10, $message10);

# Print Out Rest of Acknowledgement Page

   print "<br><br><hr><br><table><tr><td><center><b><font face=\"arial\">$fname, click <center><form><a href=\"http://www.quickcalc.com/website/cgi-bin/qcebsi.exe\"><input type=button name=B1 value=\"*Here*\"  onClick=\"top.location='http://www.quickcalc.com/website/cgi-bin/qcebsi.exe'\"></a></form></center> to download your <font color=FF0000>E</font>arly <font color=FF0000>B</font>ird <font color=FF0000>S</font>pecial.</b></center></td><td width=20></td><td><font face=arial><b>Click <a href=\"../index.html\" target=\"_parent\">HERE</a> to return to<br>the Home Page</b></td></tr></table><p>\n";
   print "</td></tr></table></center>\n";

   # Print End of HTML

   print "</body></html>\n";

   exit;

#######################
# Subroutines

# &updateDBandMail($fname1, $lname1, $email1, $message1);

sub updateDBandMail {
    my ($fnamer, $lnamer, $emailr, $messager) = @_;

    if (($fnamer ne "") && ($lnamer ne "") && ($emailr ne ""))

      {  
        open (DBFILE, ">>$dbfile") || die "Can't Open $dbfile: $!\n";
	 flock (DBFILE, 2);   #lock file

	 print DBFILE "\"$emailr\"|\"$lnamer\"|\"$fnamer\"|\"$day\"\|\"$time\"|\"$$zone\"|\"$email\"|\"$lname\"|\"$fname\"\n";
	 flock (DBFILE, 8);
	 close (DBFILE);

       # send postcard

       open (MAIL, "|$mailprog $emailr") || die "Can't open $mailprog!\n";

       print MAIL "Reply-to: $email \n";
       print MAIL "From: $email \n";
       print MAIL "Subject: Postcard from $fname $lname\n\n";

       # personalized part

       if (($messageq eq "on") and ($message1 ne ""))
           {
       	print MAIL "-----------------------------------------------------------------------------------------\n";
		print MAIL "$message1\n\n";}
        elsif ($messager ne "")
		{print MAIL "-----------------------------------------------------------------------------------------\n";
		 print MAIL "$messager\n\n";}

   print MAIL "-----------------------------------------------------------------------------------------\n";

   # generic part

   print MAIL "Dear $fnamer $lnamer,\n\n";
   print MAIL "Your gift of free QuickCalc financial calculators, sent to you by $fname $lname,\n";
   print MAIL "can be downloaded from the following web page:\n\n";
   print MAIL "       http://www.quickcalc.com\n\n"; 
   print MAIL "-----------------------------------------------------------------------------------------\n";   
   print MAIL "                    QUICKCALC FINANCIAL CALCULATORS\n";
   print MAIL "                    \"Make Informed Financial Decisions\"\n";
   print MAIL "                    URL: http://www.quickcalc.com\n";
   print MAIL "                    email: response\@quickcalc.com\n";
   print MAIL "-----------------------------------------------------------------------------------------\n";   
   close (MAIL);

   # Extend acknowledgement page

   print "<img src=\"space.gif\" hspace=10>$fnamer $lnamer, $emailr<br>\n";

	}

}


