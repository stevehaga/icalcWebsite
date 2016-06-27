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
$cgiurl = "http://207.48.84.235/cgi-bin/download.cgi";
$date_command = "/bin/date";

# Set Your Options:
$mail = 1;              # 1 = Yes; 0 = No
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
$mailprog ='/usr/lib/sendmail';             ## '/bin/sendmail';		
$recipient = 'chris_tong@adidam.org';
$recipient2 = 'chris_tong@adidam.org';   ## change to hubbell@sonic.net

# Done
##############################################################################

# Get the Date for Entry
$date = `$date_command +"%A, %B %d, %Y at %T (%Z)"`; chop($date);
$shortdate = `$date_command +"%D %T %Z"`; chop($shortdate);

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

$fname=$FORM{'fname'};
$lname=$FORM{'lname'};
$email=$FORM{'email'};

# Print Friend Page


  print "Content-type: text/html\n\n"; 
 

  print "<html>\n";
  print "<head><title>QuickCalc: QuickFriends Program</title></head>\n";
  print "<BODY TEXT=\"#000080\" BGCOLOR=\"#FFFFFF\" LINK=\"#0000EE\" \n";
  print "VLINK=\"#FF0000\" ALINK=\"#0080FF\"><font face=\"arial,helvetica\">\n";
 print qq~

<CENTER>

<P><IMG SRC=\"../title_w_new1_sm.jpg\" ALT=\"QuickCalc\" HEIGHT=76 WIDTH=285><BR>
<B><FONT FACE=\"arial\"><FONT SIZE=+1><FONT 
COLOR=\"#FF0000\">Q</FONT><FONT COLOR=\"#000080\">uick</FONT><FONT 
COLOR=\"#FF0000\">F</FONT><FONT COLOR=\"#000080\">riends</FONT><FONT 
COLOR=\"#FF0000\">
P</FONT><FONT COLOR=\"#000080\">rogram</FONT></FONT></FONT></B><BR>
<BR><BR></P>

<P><B><FONT FACE=\"arial\"><FONT COLOR=\"#000080\">
<font color=\"#FF0000\">Now</font> is your chance to surprise up to 
</FONT><FONT COLOR=\"#FF0000\">10</FONT><FONT COLOR=\"#000080\">
of your <BR> Internet friends with
a free gift:</FONT></FONT></B><BR><B><FONT FACE=\"arial\"><FONT COLOR=\"#000080\">an e-mail 
postcard, <BR>
and instructions for getting their free calculator.</FONT></FONT></B></P>


<P><B><FONT FACE=\"arial\"><FONT COLOR=\"#000080\">
Please enter each of your friends e-mail addresses on a separate line
</FONT></FONT></B></P>

<P>

<BR>


<FORM method=POST action=\"../cgi-bin/friends2.cgi\"><FONT FACE=\"arial\"><FONT SIZE=+1><FONT COLOR=\"#FF0000\">
<input type=\"hidden\" name=\"fname\" value=\"$fname\">
<input type=\"hidden\" name=\"lname\" value=\"$lname\">
<input type=\"hidden\" name=\"email\" value=\"$email\">
<! input type=\"hidden\" name=\"email\" value=\"test2\">

<P>

  
<INPUT type=text name=\"email1\" size=30>
<BR>  <INPUT type=text name=\"email2\" size=30>
<BR>  <INPUT type=text name=\"email3\" size=30>
<BR>  <INPUT type=text name=\"email4\" size=30>
<BR>  <INPUT type=text name=\"email5\" size=30>
<BR>  <INPUT type=text name=\"email6\" size=30>
<BR>  <INPUT type=text name=\"email7\" size=30>
<BR>  <INPUT type=text name=\"email8\" size=30>
<BR>  <INPUT type=text name=\"email9\" size=30>
<BR>  <INPUT type=text name=\"email10\" size=30>

</P>




<P><BR></P><CENTER><P><INPUT type=submit value=\"Send Postcards\"><IMG SRC=\"space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1><INPUT type=reset value=\"Clear Form\"></FORM></P></CENTER>
</UL>
</CENTER>
<BR><BR>
</BODY></HTML>~;