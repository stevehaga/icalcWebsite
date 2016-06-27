#!/usr/bin/perl
##############################################################################
# Download script                     Version 1                                #
# COPYRIGHT NOTICE                                                           #
# Copyright 1998 Chris Tong, Enchanted Websites. All Rights Reserved.                                                                                           
#                                                                            #
# Obtain permission before redistributing this software over the Internet or #
# in any other medium.	In all cases copyright and header must remain
# intact.
##############################################################################
#
# Updated 10/27/98 by www.bright-productions.com
# Updated 1/21/99 by www.bright-productions.com
#
##############################################################################
# Set Variables

$dbfile = "../database/download.db";
$mdbfile = "../database/mailing.db";
$cgiurl = "http://207.48.84.235/cgi-bin/download2.cgi";
$date_command = "/bin/date";

# Set Your Options:
$mail = 0;              # 1 = Yes; 0 = No
$uselog = 1;            # 1 = Yes; 0 = No
$linkmail = 1;          # 1 = Yes; 0 = No
$separator = 1;         # 1 = <hr>; 0 = <p>
$redirection = 0;       # 1 = Yes; 0 = No
$entry_order = 1;       # 1 = Newest entries added first;
                        # 0 = Newest Entries added last.
$allow_html = 1;        # 1 = Yes; 0 = No
$line_breaks = 1;	# 1 = Yes; 0 = No

# If you answered 1 to $mail or you will need to fill out 
# these variables below:
$mailprog ='/usr/lib/sendmail';                       ## '/bin/sendmail';		
$recipient = 'chris_tong@adidam.org';
$recipient2 = 'chris_tong@adidam.org';   ## change to hubbell@sonic.net

# Done
##############################################################################

# Get the Date for Entry
$date = `$date_command +"%A, %B %d, %Y at %T (%Z)"`; chop($date);
$shortdate = `$date_command +"%D %T %Z"`; 
chop($shortdate);
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

# inputs: name, email, comments, mlist

$fname=$FORM{'fname'};
$lname=$FORM{'lname'};
$email=$FORM{'email'};
$comments=$FORM{'comments'};
$mlist=$FORM{'mlist'};

# Print the Blank Response Subroutines for the Required Fields

&no_fname unless $FORM{'fname'};
&no_lname unless $FORM{'lname'};
&no_email unless $FORM{'email'};

# Remove carriage returns from TEXTAREAs.

$comments =~ s/\n//g; 

# Update the prospect database

open (DBFILE, ">>$dbfile") || die "Can't Open $dbfile: $!\n";
flock (DBFILE, 2);   #lock file

# fname, lname, email, comments

print DBFILE "\"$email\"|\"$lname\"|\"$fname\"|\"$day\"\|\"$time\"|\"$$zone\"|\"$mlist\"|\"$comments\"\n";

flock (DBFILE, 8);
close (DBFILE);

# If mailing list option checked, add prospect to the mailing list database

if ($mlist eq 'ON')

	{

	open (MDBFILE, ">>$mdbfile") || die "Can't Open $mdbfile: $!\n";
	 flock (MDBFILE, 2);   #lock file

	 # fname, lname, email, comments

	 print MDBFILE "\"$email\"|\"$lname\"|\"$fname\"|\"$day\"\|\"$time\"|\"$$zone\"|\"download\"|\"$comments\"\n";

	 flock (MDBFILE, 8);
	 close (MDBFILE);

	}

#########
# Options

# Mail Option
if ($mail eq '1') {

# Send to Chris Tong

   open (MAIL, "|$mailprog $recipient") || die "Can't open $mailprog!\n";

   print MAIL "Reply-to: $email \n";
   print MAIL "From: $email \n";
   print MAIL "Subject: Free download request\n\n";
   print MAIL "------------------------------------------------------\n";

   # name, email, comments

   print MAIL "NAME: $fname $lname \n";
   print MAIL "EMAIL: $email \n";
   print MAIL "MLIST: $mlist \n";
   print MAIL "COMMENTS: $comments \n";

   print MAIL "------------------------------------------------------\n";

   close (MAIL);

# Send to Michael Hubbell

   open (MAIL, "|$mailprog $recipient") || die "Can't open $mailprog!\n";

   print MAIL "Reply-to: $email \n";
   print MAIL "From: $email \n";
   print MAIL "Subject: Free download request\n\n";
   print MAIL "------------------------------------------------------\n";

   # name, email, comments

   print MAIL "NAME: $fname $lname \n";
   print MAIL "EMAIL: $email \n";
   print MAIL "MLIST: $mlist \n";
   print MAIL "COMMENTS: $comments \n";

   print MAIL "------------------------------------------------------\n";

   close (MAIL);

}


# Print Out Download Page

&download_page;

#######################
# Subroutines


# &no_fname unless $fname;

sub no_fname {
   print "Content-type: text/html\n\n";
   print "<html><head><title>You didn't enter your first name!</title></head>\n";
   print "<body text=\"000080\" bgcolor=\"FFFFFF\"><font face=\"arial\" color=\"000080\"><h1 align=\"center\">You didn't enter your first name!</h1>\n";
   print "<center><table width=80%><tr><td><font face=\"arial\">\n";
   print "Please press the <b>BACK</b> button on your browser and fill in your first name, so you can download your <font color=\"FF0000\"><b>FREE</b></font> calculator.</td></tr></table></body></html>\n";

   exit;
}


# &no_lname unless $lname;

sub no_lname {
   print "Content-type: text/html\n\n";
   print "<html><head><title>You didn't enter your last name!</title></head>\n";
   print "<body text=\"000080\" bgcolor=\"FFFFFF\"><font face=\"arial\" color=\"000080\"><h1 align=\"center\">You didn't enter your last name!</h1>\n";
   print "<center><table width=80%><tr><td><font face=\"arial\">\n";
   print "Please press the <b>BACK</b> button on your browser and fill in your last name, so you can download your <font color=\"FF0000\"><b>FREE</b></font> calculator.</td></tr></table></body></html>\n";

   exit;
}


# &no_email unless $email;

sub no_email {
   print "Content-type: text/html\n\n";
   print "<html><head><title>You didn't enter your email address!</title></head>\n";
   print "<body text=\"000080\" bgcolor=\"FFFFFF\"><font face=\"arial\" color=\"000080\"><h1 align=\"center\">You didn't enter your email address!</h1>\n";
 print "<center><table width=80%><tr><td><font face=\"arial\">\n";
   print "Please press the <b>BACK</b> button on your browser and fill in your email address, so you can download your <font color=\"FF0000\"><b>FREE</b></font> calculator.</td></tr></table></body></html>\n";

   exit;
}

#-----------------------------------------------------
# Redirection Option
sub download_page {

   # Print Beginning of HTML
   print "Content-Type: text/html\n\n";
   print "<html><head><title>Your form has been successfully submitted.</title></head>\n";
   print "<BODY TEXT=\"#000080\" BGCOLOR=\"#FFFFFF\" LINK=\"#0000EE\" 
VLINK=\"#FF0000\" ALINK=\"#0080FF\"><font face=\"arial,helvetica\">\n";

   # Print Response

   print "<center><img src=\"../title_w_new1_sm.jpg\" width=285 height=76 alt=\"QuickCalc\"></center><br><br>\n";
   print "<center><table width=90%><tr><td>\n";  
   print "<font face=\"arial\"><b>$fname,<br><br>\n";
   print "To receive your <font color=FF0000>E</font>arly <font color=FF0000>B</font>ird <font color=FF0000>S</font>pecial Offer \n";
   print "and to send free Calculators to your friends, Click <center><FORM method=POST action=\"genfriend3.cgi\">\n";
   print "<input type=\"hidden\" name=\"fname\" value=\"$fname\">\n";
   print "<input type=\"hidden\" name=\"lname\" value=\"$lname\">\n";
   print "<input type=\"hidden\" name=\"email\" value=\"$email\">\n";
   print "<INPUT type=submit value=\"*Here*\"></FORM></center>\n";
   print "<br><center>OR</center><br><br>\n"; 
   print "To just receive your <font color=FF0000>E</font>arly <font color=FF0000>B</font>ird <font color=FF0000>S</font>pecial Offer Click  <center><form><a href=\"quickcalc_demo_v1.exe\"><input type=button name=B1 value=\"*Here*\"  onClick=\"top.location='quickcalc_demo_v1.exe'\"></a></form></center><br><br>\n";
   print "<p></td></tr></table></center>\n";

   # Print End of HTML

   print "</body></html>\n";

   exit;
}
