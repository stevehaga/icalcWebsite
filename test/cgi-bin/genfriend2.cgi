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
#
##############################################################################
# Set Variables

$dbfile = "../database/download.db";
$cgiurl = "http://www.quickcalc.com/cgi-bin/download.cgi";
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
$mailprog = '/bin/sendmail';		## was /usr/lib/sendmail
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

   print "Content-Type: text/html\n\n";
   print "<html><head><title>QuickCalc: QuickFriends Program</title></head>\n";
   print "<BODY TEXT=\"#000080\" BGCOLOR=\"#FFFFFF\" LINK=\"#0000EE\" 
VLINK=\"#FF0000\" ALINK=\"#0080FF\"><font face=\"arial,helvetica\">\n";

   print "<CENTER><P><IMG SRC=\"../title_w_new1_sm.jpg\" ALT=\"QuickCalc\" HEIGHT=76 WIDTH=285><BR>\n";
   print "<B><FONT FACE=\"arial\"><FONT SIZE=+1><FONT \n";
   print "COLOR=\"#FF0000\">Q</FONT><FONT COLOR=\"#000080\">uick</FONT><FONT \n";
   print "COLOR=\"#FF0000\">F</FONT><FONT COLOR=\"#000080\">riends</FONT><FONT \n";
   print "COLOR=\"#FF0000\">\n";

   print "P</FONT><FONT COLOR=\"#000080\">rogram</FONT></FONT></FONT></B><BR>\n";

   print "<BR><BR></P></CENTER>\n";

   print "<UL><UL><P><B><FONT FACE=\"arial\"><FONT COLOR=\"#000080\"><font\n";

   print "color=\"#FF0000\">Now</font> is your chance to surprise up to \n";
   print "</FONT><FONT COLOR=\"#FF0000\">10</FONT><FONT COLOR=\"#000080\">\n";

   print "of your Internet friends <BR> with\n";

   print "a free gift:</FONT></FONT></B></P>\n";
   print "<UL><P><BR><B><FONT FACE=\"arial\"><FONT COLOR=\"#000080\">an e-mail \n";
   print "postcard with a message\n";

   print "from you, <BR>\n";

   print "and instructions for getting their free calculator.</FONT></FONT></B></P>\n";

   print "</UL></UL><P><BR><BR>\n";

   print "<FORM method=POST action=\"../cgi-bin/friends.cgi\"><FONT FACE=\"arial\"><FONT SIZE=+1><FONT COLOR=\"#FF0000\">\n";

   print "<input type=\"hidden\" name=\"fname\" value=\"$fname\">\n";
   print "<input type=\"hidden\" name=\"lname\" value=\"$lname\">\n";
   print "<input type=\"hidden\" name=\"email\" value=\"$email\">\n";


   print "<B>1.</B></FONT><FONT COLOR=\"#000080\">first name <INPUT type=text name=\"fname1\" \n";
   print "size=20><IMG SRC=\"space.gif\" HSPACE=5 HEIGHT=1 \n";
   print "WIDTH=1></FONT></FONT><B><FONT COLOR=\"#000080\">last\n";

   print "name</FONT><FONT COLOR=\"#FF0000\"> </FONT></B></FONT><INPUT \n";
   print "type=text name=\"lname1\" size=20></P>\n";
print "<P><IMG SRC=\"space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
print "address </FONT></FONT></B><INPUT type=text name=\"email1\" size=50></P>\n";
 print "<UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our
message</FONT></FONT></FONT><BR></P>\n";
 print "<UL><P><TEXTAREA name=\"message1\" ROWS=4 COLS=40></TEXTAREA></P>\n";
 print "<P><INPUT type=\"checkbox\" name=\"messageq\" checked><IMG SRC=\"space.gif\" HSPACE=10 HEIGHT=1 WIDTH=1><FONT FACE=\"arial\"><FONT COLOR=\"#000080\">Use\n";
 print "the same message for every postcard.</FONT></FONT><BR><BR><BR></P></UL></UL>\n";
print "<P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">2. </FONT></B><FONT COLOR=\"#000080\">first\n";
 print "name <INPUT type=text name=\"fname2\" \n";
 print "size=20><IMG SRC=\"space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1>last\n";
 print "name</FONT></FONT><FONT COLOR=\"#FF0000\"> </FONT></FONT><INPUT type=text name=\"lname2\" size=20></P>\n";
 print "<P><IMG SRC=\"/space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
 print "address </FONT></FONT></B><INPUT type=text name=\"email2\" size=50><BR>\n";
 print "</P><UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our\n";
 print "message</FONT></FONT></FONT></P>\n";
 print "<P><TEXTAREA name=\"message2\" ROWS=4 COLS=40></TEXTAREA></P></UL>\n";
 print "<P><BR><BR><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">3. </FONT></B><FONT COLOR=\"#000080\">first\n";
 print "name<B> <INPUT type=text name=\"fname3\" size=20><IMG SRC=\"/space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1></B></FONT></FONT><B><FONT COLOR=\"#000080\">last\n";
 print "name</FONT><FONT COLOR=\"#FF0000\"> </FONT></B></FONT><INPUT type=text name=\"lname3\" size=20></P>\n";
 print "<P><IMG SRC=\"/space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
 print "address </FONT></FONT></B><INPUT type=text name=\"email3\" size=50><BR>\n";
 print "</P><UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our\n";
 print "message</FONT></FONT></FONT></P>\n";
 print "<P><TEXTAREA name=\"message3\" ROWS=4 COLS=40></TEXTAREA></P></UL>\n";
 print "<P><BR><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">4. </FONT></B><FONT COLOR=\"#000080\">first\n";
 print "name<B> <INPUT type=text name=\"fname4\" size=20><IMG SRC=\"/space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1></B></FONT></FONT><B><FONT COLOR=\"#000080\">last\n";
 print "name</FONT><FONT COLOR=\"#FF0000\"> </FONT></B></FONT><INPUT type=text name=\"lname4\" size=20></P>\n";
 print "<P><IMG SRC=\"/space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
 print "address </FONT></FONT></B><INPUT type=text name=\"email4\" size=50><BR>\n";
 print "</P><UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our\n";
 print "message</FONT></FONT></FONT></P>\n";
 print "<P><TEXTAREA name=\"message4\" ROWS=4 COLS=40></TEXTAREA></P></UL>\n";
 print "<P><BR><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">5. </FONT></B><FONT COLOR=\"#000080\">first\n";
 print "name<B> <INPUT type=text name=\"fname5\" size=20><IMG SRC=\"/space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1></B></FONT></FONT><B><FONT COLOR=\"#000080\">last\n";
 print "name</FONT><FONT COLOR=\"#FF0000\"> </FONT></B></FONT><INPUT type=text name=\"lname5\" size=20></P>\n";
 print "<P><IMG SRC=\"/space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
 print "address </FONT></FONT></B><INPUT type=text name=\"email5\" size=50><BR></P>\n";
 print "<UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our\n";
 print "message</FONT></FONT></FONT></P>\n";
 print "<P><TEXTAREA name=\"message5\" ROWS=4 COLS=40></TEXTAREA></P></UL>\n";
 print "<P><BR><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">6. </FONT></B><FONT COLOR=\"#000080\">first\n";
 print "name<B> <INPUT type=text name=\"fname6\" size=20><IMG SRC=\"/space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1></B></FONT></FONT><B><FONT COLOR=\"#000080\">last\n";
 print "name</FONT><FONT COLOR=\"#FF0000\"> </FONT></B></FONT><INPUT type=text name=\"lname6\" size=20></P>\n";
 print "<P><IMG SRC=\"/space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
 print "address </FONT></FONT></B><INPUT type=text name=\"email6\" size=50><BR>\n";
 print "</P><UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our\n";
 print "message</FONT></FONT></FONT></P>\n";
 print "<P><TEXTAREA name=\"message6\" ROWS=4 COLS=40></TEXTAREA></P></UL>\n";
 print "<P><BR><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">7. </FONT></B><FONT COLOR=\"#000080\">first\n";
 print "name<B> <INPUT type=text name=\"fname7\" size=20><IMG SRC=\"/space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1></B></FONT></FONT><B><FONT COLOR=\"#000080\">last\n";
 print "name</FONT><FONT COLOR=\"#FF0000\"> </FONT></B></FONT><INPUT type=text name=\"lname7\" size=20></P>\n";
 print "<P><IMG SRC=\"/space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
 print "address </FONT></FONT></B><INPUT type=text name=\"email7\" size=50><BR>\n";
 print "</P><UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our\n";
 print "message</FONT></FONT></FONT></P>\n";
 print "<P><TEXTAREA name=\"message7\" ROWS=4 COLS=40></TEXTAREA></P></UL>\n";
 print "<P><BR><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">8. </FONT></B><FONT COLOR=\"#000080\">first\n";
 print "name<B> <INPUT type=text name=\"fname8\" size=20><IMG SRC=\"/space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1></B></FONT></FONT><B><FONT COLOR=\"#000080\">last\n";
 print "name</FONT><FONT COLOR=\"#FF0000\"> </FONT></B></FONT><INPUT type=text name=\"lname8\" size=20></P>\n";
 print "<P><IMG SRC=\"/space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
 print "address </FONT></FONT></B><INPUT type=text name=\"email8\" size=50><BR>\n";
 print "</P><UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our\n";
 print "message</FONT></FONT></FONT></P>\n";
 print "<P><TEXTAREA name=\"message8\" ROWS=4 COLS=40></TEXTAREA></P></UL>\n";
 print "<P><BR><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">9. </FONT></B><FONT COLOR=\"#000080\">first\n";
 print "name<B> <INPUT type=text name=\"fname9\" size=20><IMG SRC=\"/space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1></B></FONT></FONT><B><FONT COLOR=\"#000080\">last\n";
 print "name</FONT><FONT COLOR=\"#FF0000\"> </FONT></B></FONT><INPUT type=text name=\"lname9\" size=20></P>\n";
 print "<P><IMG SRC=\"/space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
 print "address </FONT></FONT></B><INPUT type=text name=\"email9\" size=50><BR></P>\n";
 print "<UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our\n";
 print "message</FONT></FONT></FONT></P>\n";
 print "<P><TEXTAREA name=\"message9\" ROWS=4 COLS=40></TEXTAREA></P></UL>\n";
 print "<P><BR><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">10. </FONT></B><FONT COLOR=\"#000080\">first\n";
 print "name<B> <INPUT type=text name=\"fname10\" size=20><IMG SRC=\"space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1></B></FONT></FONT><B><FONT COLOR=\"#000080\">last\n";
 print "name</FONT><FONT COLOR=\"#FF0000\"> </FONT></B></FONT><INPUT type=text name=\"lname10\" size=20></P>\n";
 print "<P><IMG SRC=\"space.gif\" HSPACE=20 HEIGHT=1 WIDTH=1><B><FONT FACE=\"arial\"><FONT COLOR=\"#FF0000\"><FONT SIZE=+1>E</FONT></FONT><FONT COLOR=\"#000080\">-mail\n";
 print "address </FONT></FONT></B><INPUT type=text name=\"email10\" size=50><BR></P>\n";
 print "<UL><P><FONT FACE=\"arial\"><FONT SIZE=+1><B><FONT COLOR=\"#FF0000\">Y</FONT></B><FONT COLOR=\"#000080\">our\n";
 print "message</FONT></FONT></FONT></P>\n";
 print "<P><TEXTAREA name=\"message10\" ROWS=4 COLS=40></TEXTAREA></P></UL>\n";
 print "<P><BR></P><CENTER><P><INPUT type=submit value=\"Send Postcards\"><IMG SRC=\"space.gif\" HSPACE=5 HEIGHT=1 WIDTH=1><INPUT type=reset value=\"Clear Form\"></FORM></P></CENTER>\n";
 print "</UL><CENTER><P>\n";
 print "<HR WIDTH=\"100%\"></CENTER>\n";
 print "<CENTER><TABLE WIDTH=\"100%\" ><TR><TD WIDTH=\"20\"></TD>\n";
 print "<TD><I><FONT FACE=\"Arial\"><FONT SIZE=-1><FONT COLOR=\"#000080\">Copyright\n";
 print "&copy; 1998 by <B>Quick</B></FONT><B><FONT COLOR=\"#FF0000\">C</FONT><FONT COLOR=\"#000080\">alc\n";
 print "Products</FONT></B><FONT COLOR=\"#000080\">. All rights reserved worldwide.\n";
 print "<BR>Please direct comments and questions about this website to <A HREF=\"mailto:response\@quickcalc.com\">response\@quickcalc.com</A>.</FONT></FONT></FONT></I></TD>\n";
 print "<TD WIDTH=\"10\"></TD>\n";
 print "<TD><IMG SRC=\"../logo.gif\" HEIGHT=71 WIDTH=92></TD>\n";
 print "<TD WIDTH=\"20\"></TD>\n";
 print "</TR></TABLE></CENTER>\n";
 print "</BODY></HTML>\n";


exit;
