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
# Set Variables

$dbfile = "../database/order.db";
$mdbfile = "../database/mailing.db";
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

# inputs: earlyb

$earlyb=$FORM{'earlyb'};

if ($earlyb ne "on")
	{print "Content-type: text/html\n\n";
   	print "<html><head><title>You didn't order anything!</title></head>\n";
   	print "<body text=\"000080\" bgcolor=\"FFFFFF\"><font face=\"arial\" color=\"000080\"><h1 align=\"center\">You didn't order anything!</h1>\n";
   	print "<center><table width=80%><tr><td><font face=\"arial\">\n";
   	print "Please press the <b>BACK</b> button on your browser and check the \"Early Bird\" Special box before submitting your order.</td></tr></table></body></html>\n";
	exit;}

# print "info solicitation" page

print "Content-Type: text/html\n\n";
print <<end_of_order_form;
<html>
<head>
<title>Order form</title></head>
<BODY TEXT="#000080" BGCOLOR="#FFFFFF" LINK="#0000EE" 
VLINK="#FF0000" ALINK="#0080FF"><font face="arial,helvetica">
<CENTER><P><IMG SRC="../title_short.jpg" alt="QuickCalc" HEIGHT=52 WIDTH=275><BR>
<B><FONT FACE="arial"><FONT SIZE=+1><FONT COLOR="#FF0000">R</FONT><FONT 
COLOR="#000080">egistration
</FONT><FONT COLOR="#FF0000">F</FONT><FONT COLOR="#000080">orm</FONT></FONT></FONT></B></P></CENTER>

<font face="arial">
<FORM method=POST action="../cgi-bin/submit.cgi">
<center>
<table border="0" width=500>
<tr>
<td colspan=2><font face="arial">
<br><br>
Please enter the following information so we can register you for your incredible
<b>\$10</b> "Early Bird" Special, using our "Bill Me Later" option:<br><br>
</td>
</tr>

                <tr>

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">F</font>irst name:</b> </small></td>

                  <td align="left" BGCOLOR="D3D3D3"><input type="text" 
name="FNAME" SIZE="45"> </td>

                </tr>

                <tr>

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">L</font>ast name: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3"><input type="text" name="LNAME" SIZE="45"> </td>

                </tr>

                <tr>

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">A</font>ddress: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3"><input type="text" name="ADDRESS1" SIZE="45"> </td>

                </tr>

                <tr>

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">A</font>ddress: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3"><input type="text" name="ADDRESS2" SIZE="45"> </td>

                </tr>

                <tr>

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">C</font>ity: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3"><input type="text" name="CITY" SIZE="45"> </td>

                </tr>

                <tr>

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">S</b>tate or Province: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3"><select name="D4" size="1">

                    <option VALUE="AL">Alabama</option>

                    <option VALUE="AK">Alaska</option>

                    <option VALUE="AZ">Arizona</option>

                    <option VALUE="AR">Arkansas</option>

                    <option VALUE="CA">California</option>

                    <option VALUE="CO">Colorado</option>

                    <option VALUE="CT">Connecticut</option>

                    <option VALUE="DE">Delaware</option>

                    <option VALUE="DC">District of Columbia</option>

                    <option VALUE="FL">Florida</option>

                    <option VALUE="GA">Georgia</option>

                    <option VALUE="HI">Hawaii</option>

                    <option VALUE="ID">Idaho</option>

                    <option VALUE="IL">Illinois</option>

                    <option VALUE="IN">Indiana</option>

                    <option VALUE="IA">Iowa</option>

                    <option VALUE="KS">Kansas</option>

                    <option VALUE="KY">Kentucky</option>

                    <option VALUE="LA">Louisiana</option>

                    <option VALUE="ME">Maine</option>

                    <option VALUE="MD">Maryland</option>

                    <option VALUE="MA">Massachusetts</option>

                    <option VALUE="MI">Michigan</option>

                    <option VALUE="MN">Minnesota</option>

                    <option VALUE="MS">Mississippi</option>

                    <option VALUE="MO">Missouri</option>

                    <option VALUE="MT">Montana</option>

                    <option VALUE="NE">Nebraska</option>

                    <option VALUE="NV">Nevada</option>

                    <option VALUE="NH">New Hampshire</option>

                    <option VALUE="NJ">New Jersey</option>

                    <option VALUE="NM">New Mexico</option>

                    <option VALUE="NY">New York</option>

                    <option VALUE="NC">North Carolina</option>

                    <option VALUE="ND">North Dakota</option>

                    <option VALUE="OH">Ohio</option>

                    <option VALUE="OK">Oklahoma</option>

                    <option VALUE="OR">Oregon</option>

                    <option VALUE="PA">Pennsylvania</option>

                    <option VALUE="PR">Puerto Rico</option>

                    <option VALUE="RI">Rhode Island</option>

                    <option VALUE="SC">South Carolina</option>

                    <option VALUE="SD">South Dakota</option>

                    <option VALUE="TN">Tennessee</option>

                    <option VALUE="TX">Texas</option>

                    <option VALUE="UT">Utah</option>

                    <option VALUE="VT">Vermont</option>

                    <option VALUE="VA">Virginia</option>

                    <option VALUE="WA">Washington</option>

                    <option VALUE="WV">West Virginia</option>

                    <option VALUE="WI">Wisconsin</option>

                    <option VALUE="WY">Wyoming</option>

                    <option VALUE="Other">Other</option>

                  </select> </td>

                </tr>

                <tr>

                  <td align="right" BGCOLOR="D3D3D3" valign="top"><font 
face="arial"><small><b><font color="FF0000">C</font>ountry: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3" valign="top"><div align="center"><center><p><select name="D7" size="1">

                    <option selected value="USA">USA</option>

                    <option value="Argentina">Argentina</option>

                    <option value="Austria">Austria</option>

                    <option value="Australia">Australia</option>

                    <option value="Belgium">Belgium</option>

                    <option value="Brazil">Brazil</option>

                    <option value="Canada">Canada</option>

                    <option value="Chile">Chile</option>

                    <option value="China">China</option>

                    <option value="Colombia">Colombia</option>

                    <option value="Czech Republic">Czech Republic</option>

                    <option value="Denmark">Denmark</option>

                    <option value="Finland">Finland</option>

                    <option value="France">France</option>

                    <option value="Germany">Germany</option>

                    <option value="Greece">Greece</option>

                    <option value="Hong Kong">Hong Kong</option>

                    <option value="Hungary">Hungary</option>

                    <option value="India">India</option>

                    <option value="Ireland">Ireland</option>

                    <option value="Israel">Israel</option>

                    <option value="Italy">Italy</option>

                    <option value="Japan">Japan</option>

                    <option value="Malaysia">Malaysia</option>

                    <option value="Mexico">Mexico</option>

                    <option value="Netherlands">Netherlands</option>

                    <option value="New Zealand">New Zealand</option>

                    <option value="North Korea">North Korea</option>

                    <option value="Norway">Norway</option>

                    <option value="Peru">Peru</option>

                    <option value="Poland">Poland</option>

                    <option value="Portugal">Portugal</option>

                    <option value="Russia">Russia</option>

                    <option value="Scotland">Scotland</option>

                    <option value="Singapore">Singapore</option>

                    <option value="Slovenia">Slovenia</option>

                    <option value="South Africa">South Africa</option>

                    <option value="South Korea">South Korea</option>

                    <option value="Spain">Spain</option>

                    <option value="Sweden">Sweden</option>

                    <option value="Switzerland">Switzerland</option>

                    <option value="Taiwan">Taiwan</option>

                    <option value="Turkey">Turkey</option>

                    <option value="United Kingdom">United Kingdom</option>

                    <option value="USA">USA</option>

                  </select><br><font face="arial">

                  <small>Country, required if State/Province is &quot;Other&quot; </small></td>

                </tr>

                <tr align="center">

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">Z</font>ip or Postal Code: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3"><input type="text" name="ZIP" SIZE="45"> </td>

                </tr>

                <tr align="center">

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">E</font>-Mail Address: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3"><input type="text" name="EMAIL" SIZE="45"> </td>

                </tr>

                <tr align="center">

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">P</font>hone: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3"><input type="text" name="PHONE" SIZE="45"> </td>

                </tr>

                <tr align="center">

                  <td align="right" BGCOLOR="D3D3D3"><font 
face="arial"><small><b><font color="FF0000">F</font>ax: </b></small></td>

                  <td align="left" BGCOLOR="D3D3D3"><input type="text" name="FAX" SIZE="45"> </td>

                </tr>

<tr>
<td align=top>
<INPUT type=checkbox name="mlist" checked></td>
<td><br><br><b><FONT FACE="arial"><FONT COLOR="#FF0000">YES</FONT>,
please add me to the Quick<FONT COLOR="#FF0000">C</FONT>alc mailing list, so I
can be notified about 
your newest calculators and special offers.</FONT></B>
</td>
</tr>

                <tr align="center">

                  <td align="center" colspan="2"><br><br><input type="submit" value=" Submit "><img
src="space.gif" hspace=10><input type="Reset" value=" Clear "> </small></td>

                </tr>

              </table>
</center>
</form>

</body>
</html>
end_of_order_form

