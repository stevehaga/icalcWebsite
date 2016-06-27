#!/usr/bin/perl
# cgi-bin access counter program
# Version 4.0.5
#
# Copyright (C) 1995 George Burgyan
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# A full copy of the GNU General Public License can be retrieved from
# http://www.webtools.org/counter/copying.html
#
# gburgyan@webtools.org
#
# George Burgyan
# 1380 Dill Road
# South Euclid, OH 44121
#
# For more information look at http://www.webtools.org/counter/########################################################################
#
#   CHANGE THESE TO SUIT YOUR SITE
#
# The default language option (english, french, swedish)
$default_lang = "english";
# The name of the file to use.  You should probably give this an absolute path
$FileName = "access_count3";
# Replace with a list of regular expression IP addresses that we
# are supposed to ignore.  If you don't know what this means, just use
# "\." instead of periods.  Comment out entirely to ignore nothing.
#@IgnoreIP = ("199\.18\.203\..*",
#	      "199\.18\.159\.1",
#	      );
@IgnoreIP = ();
# Aliases: Set this up so that diffent pages will all yield the same
# count.  For instance, if you have a link like "index.html -> home.html"
# set it up like ("/index.html", "/home.html").  Make sure you give a full
# path to it. This will treat "/index.html" as if it were "/home.html".
#%Aliases = ("/fakename.html", "/realname.html",
#            "/index.html", "/home.html",
#	    );
%Aliases = ();
# AUTOMATICALLY SET BY INSTALL!!   Modify only if necessary!!!
#
# BaseName: set to whatever you have counter installed as.  This is
# used to derive the arguments.  No not touch the next comment.
### AUTOMAGIC ###
$BaseName = "counter";
# counter  or  counterbanner  or  counterfiglet
#
# Outputs the number of times a specific page has been accessed.
# The output depends on which page 'called' it, and what the program
# is named:
#
# The counter can "take arguments" via its name.  That is, if you tack
# -arg to the end of the program name, -arg is taken to be an argument.
# For example, if you call the counter 'counter-ord', '-ord' is considered
# an argument, and an ordinal count (1st, 2nd, 3rd, ...) will be printed
# instead of (1, 2, 3, ...).  Note that counterord does the same thing as
# counter-ord for backward compatibility.
#
# Currently recognized arguments:
#
#  -f=font	sets "font" to be the font for figlet
#  -lang=lang   sets the language used to ordinalize to "lang"
#  -nc		no count; don't to write the incremented count back to the file
#  -nl		no link; don't automatically generate a link
#  -nd          no display; don't display anything, just count
#  -ord		make an ordinal count instead of regular
#  -doc=document override the DOCUMENT_URI environment variable
#
# Example:  counterfiglet-ord-f=bigfont-nc
#
# This will cause the counter to call figlet as the output routine, printing
# in a big font an ordinal count, without updating the access count file.
# Note that the order of arguments is irrelevant so long as you spell the
# file name correctly.  It is generally assumed that the ability to take
# different arguments/use different output routines is done with symlinks:
# i.e. ln -s counter counterfiglet-ord-f=bigfont-nc
#
# More complete documentation can be found at
# http://www.webtools.org/counter/
#
########################################################################
#
# Thing that shouldn't really need changing, but are configurable anyway.
#
# Maximum number of times to try to lock the file.
# Each try is .1 second.  Try for 1 second.
$MaxTries = 10;
# Set this to point to something, or comment it out, and it
# won't be a link at all.\
$Link = "http://www.webtools.org/counter/";
# Whether or not to use locking.  If perl complains that flock is not
# defined, change this to 0.  Not *really* necessary because we check
# to make sure it works properly.
$UseLocking = 1;
# What version of the counter file format are we using?
$FileVersion = "02.000";
# Common names of the counter to install...
@CommonExtensions = ("-ord",	  # Ordinam
		     "figlet",	  # Figlet'ed
		     "figlet-ord",# Ordinal figlet
		     "banner",    # Bannered
		     "banner-ord",# Ordinal banner
		     );
#
#########################################################################
#
# Misc documents to refer people to in case of errors.
#
$CreateFile = "<a href=\"http://www.webtools.org/counter/faq.html#create\">[Error Creating Counter File -- Click for more info]</a>";
$AccessRights = "<a href=\"http://www.webtools.org/counter/faq.html#rights\">[Error Opening Counter File -- Click for more info]</a>";
$TimeoutLock = "[Timeout locking counter file]";
$BadVersion = "<a href=\"http://www.webtools.org/counter/\">[Version access_count newer than this program.  Please upgrade.]</a>";
#########################################################################
#
# The actual program!
### Stage 1
###
### Parse the arguments...  (just ignore this part)
# Get arguments from program name.  Argh...what a horrible way to do it!
$prog = $0;
$prog =~ s/(\.cgi|\.pl)//;      #strip .cgi|.pl name extension
$prog =~ s!^(.*/)!!;		# separate program name
$prog =~ s/\\(.)/sprintf("%%%02x", ord($1))/ge;	# quote \c to %xx
($printer, @args) = split(/-/, $prog);	# args are separated by dashes
$printer =~ s/%(..)/pack("c", hex($1))/ge; # unquote printer function name
$printer =~ s/$BaseName/counter/; # Make it cannonical.
# This gets path info, which is only applicable if you are using our
# ssis script (see above).  This makes counter/ord the same as counter-ord
push(@args, split("/", $ENV{"PATH_INFO"})) if $ENV{"PATH_INFO"};
# put them in assoc array %arg
foreach (@args)	# means do this for each element in the array
{
    s/%(..)/pack("c", hex($1))/ge;	# unquote %xx
    /^([^=]*)=?(.*)$/;			# extract "=" part, if any
    $arg{$1} = $2 ? $2 : 1;
}
if ($ARGV[0] eq '-install') {
    &CheckPerl;
    &SetBaseName;
    &MakeCommon(0);
    exit(0);
}
if ($ARGV[0] eq '-installforce') {
    &CheckPerl;
    &SetBaseName;
    &MakeCommon(1);
    exit(0);
}
if ($ARGV[0] eq '-unlock') {
    open(FILE,"$FileName");
    &UnlockFile(FILE);
    exit(0);
}
undef $Link if $arg{'nl'};	# make link?

### Stage 2
###
### Print out the header
# Print out the header
print "Content-type: text/html\n\n";
### Stage 3
###
### Open the access_count file for read-write taking all the precautions
# Make sure the file exists:
if (!(-f $FileName)) {
    if (!open (COUNT,">$FileName")) {
	# Can't create the file
	print $CreateFile;
	exit 1;
    } else {
	# We got the file, print out the version number
	print COUNT "$FileVersion\n";
	$version = 2;
    }
} else {
    if (!((-r $FileName) && (-w $FileName))) {
	# Make sure that we can in fact read and write to the file in
	# question.  If not, direct them to the FAQ.
	print $AccessRights;
	exit 1;
    }
    if (!open (COUNT,"+<$FileName")) {	# Now make sure it *really* opens
	print $AccessRights;	        # ...just in case...
	exit 1;
    }
    # Try to read in a version number
    $version = <COUNT>;
    if (!($version =~ /^\d+.\d+$/)) {
	# No version number, assume version 1 and reset the file.
	$version = 1;
	seek(COUNT,0,0);
    }
}
# This is for the future: the access_count file will have a version number.
if ($version > 2) {
    print $BadVersion;
    exit 1;
}

### Stage 4
###
### Attempt to lock the file


$lockerror = &LockFile(COUNT);
# You would figure that $MaxTries would equal 0 if it didn't work.  The
# post-decrement takes it to -1 when the loop finally exits.
if ($lockerror) {
    print $TimeoutLock;
    exit(0);
}


### Stage 5
###
### Check if we need to update the file to a newer version

if ($version < 2) {
    &UpdateVersion1;
}


### Stage 6
###
### Convert the information the server gave us into the document
### identifier.

# Make sure perl doesn't spit out warnings...
if (defined $ENV{'DOCUMENT_URI'}) {
    $doc_uri = $ENV{'DOCUMENT_URI'};
} else {
    $doc_uri = "";
}

# Campatibility: Version 2 files have the server name in front if and
# only if it doesn't have a "~" in it.

$old_uri = $doc_uri;

# Add the server name in front to support multi-homed hosts if and only if
# it doesn't have a "~" in it.  (usernames are global in most multi-homed
# settings
if (defined $ENV{'SERVER_NAME'} && !($doc_uri =~ /~/)) {
    $doc_uri = $ENV{'SERVER_NAME'} . "/" . $doc_uri;
}

if (defined $arg{'doc'}) {
    $doc_uri = $arg{'doc'};
}

$doc_uri = $Aliases{$doc_uri} if defined $Aliases{$doc_uri};


### Stage 7
###
### Find the relevant place in the file

$location = tell COUNT;
while ($line = <COUNT>) {
    # Read the file line-by-line.
    if (($uri,$accesses) = ($line =~ /^'(\S*)' (\d\d\d\d\d\d\d\d\d\d)$/)) {
	# An old line
	if ($uri eq $old_uri) {
	    &ConvertDocV1($doc_uri,$old_uri,$accesses,$location);
	    last;
	}
    } elsif (($uri,$accesses,$flags) = ($line =~ /^'(\S*)' (\d\d\d\d\d\d\d\d\d\d) (\w\w\w\w)$/)) {
	# A new line
	if ($uri eq $doc_uri) {
	    $flags = hex($flags);
	    last;
	}
    }
   last if ($uri eq $doc_uri);
    $location = tell COUNT;
    
    #reset the fields
    $accesses = 0;
    $flags = 0;
}


### Stage 8
###
### Update the access count of the file

$accesses += 1;	# *NOT* '++' because we don't want '++'s magic


### Stage 9
###
### Figure out what to print out

# If we have to ordinalize, do it now.
if (defined $arg{'ord'}) {
    if (defined $arg{'lang'}) {
	$ord = eval("&ordinalize_$arg{lang}($accesses)");
    } else {
	$ord = &ordinalize($accesses);
    }
} else {
    $ord = "";
}
$to_print = $accesses . $ord;

# Give it to the printer function to actually produce the output from the
# ascii text that we have (to_print)
($count, $nLink) = eval("&output_$printer('$to_print')");
# If the above line gave us an error, default to just the text.
if ($@) {
    ($count, $nLink) = &output_counter($to_print);
}

### Stage 10
###
### Now we actually tell the browser what the count is.

if (! $arg{"nd"} ) {		# If we print anything
    # Print out a link to something informative (if we were requested to)
    # print "<a href=\"$nLink\">" if $nLink;
    print $count;
    # print "</a>" if $nLink;
}


### Stage 11
###
### Check if we are supposed to update the count in the file.  (ie. we're
### not ignoring the host that just accessed us)

# Make sure we are not ignoring the host:

$ignore = 0;
$ignore = grep($ENV{"REMOTE_ADDR"} =~ /$_/, @IgnoreIP) if defined ($ENV{"REMOTE_ADDR"});
$ignore = $ignore || $arg{"nc"};

### Stage 12
###
### Actually write the updated information back to the file

if (!$ignore)			# If we aren't ignoring this access
{
    # Now update the counter file
    seek(COUNT, $location, 0);
    $longaccesses = sprintf("%010.10d", $accesses);
    $hexflags = sprintf("%04.4x", $flags);
    print COUNT "'$doc_uri' $longaccesses $hexflags\n";
}

&UnlockFile(COUNT);

close COUNT;

#######################################################################
#
# Support functions
#

# translate_output
#
# Quote any special characters with HTML quoting.

sub translate_output {
    local($string) = @_;

    $_ = $string;
  
    s/è/&egrave;/g;

    return $_;
}

sub LockFile {
    local(*FILE) = @_;
    local($TrysLeft) = $MaxTries;

    if ($UseLocking) {
	# Try to get a lock on the file
	while ($TrysLeft--) {
	    
	    # Try to use locking, if it doesn't use locking, the eval would
	    # die.  Catch that, and don't use locking.

	    # Try to grab the lock with a non-blocking (4) exclusive (2) lock.
	    # (4 | 2 = 6)
	    $lockresult = eval("flock(COUNT,6)");

	    if ($@) {
		$UseLocking = 0;
		last;
	    }

	    if (!$lockresult) {
		select(undef,undef,undef,0.1); # Wait for 1/10 sec.
	    } else {
		last;		# We have gotten the lock.
	    }
	}
    }

    if ($TrysLeft >= 0) {
	# Success!
	return 0;
    } else {
	return -1;
    }
}

sub UnlockFile {
    local(*FILE) = @_;

    if ($UseLocking) {
	flock(FILE,8);			# Unlock the file.
    }
}


####################################################################
#
# Installation helpers
#


# SetBaseName
#
# Change the counter program itself to set the basename

sub SetBaseName {
    local($name) = $0;

    $name =~ s/^.*\/([^\/]+)$/$1/; # Strip off any of the path
    
    if ($name eq $BaseName) {	# The way we're set up now!!!
	return;			# Don't need to change a thing.
    }
    
    if (!open(COUNTERFILE, "+<$0")) {
	print "Can't modify program.  Set \$BaseName manually.\n";
	return;
    }

    print "Configuring \$BaseName variable...\n";

    local($oldsep) = $/;
    undef($/);

    local($program) = <COUNTERFILE>;
    
    # The next line does all the magic.
    $program =~ s/\#\#\# AUTOMAGIC \#\#\#\n\$BaseName = \"[^\"]+\";\n/\#\#\# AUTOMAGIC \#\#\#\n\$BaseName = \"$name\";\n/;

    seek(COUNTERFILE,0,0) || return;
    truncate(COUNTERFILE,0);
    print COUNTERFILE $program;
    close COUNTERFILE;
}
	
# CheckPerl
#
# Make sure that the "#! /[path]/perl" points to something real...

sub CheckPerl {
    if (!open(COUNTERFILE, "<$0")) {
	print "Can't check to make sure Perl is in the right place.\n";
	return;
    }
    print "Checking to make sure Perl is found properly...\n";

    $firstline = <COUNTERFILE>;
    ($command) = ($firstline =~ /^\#! *([^\s]+) *$/);
    close(COUNTERFILE);

    if (! -x $command) {
	print "The location of Perl is misconfigured.  Please edit the\n";
	print "first line of this program to point to the locally installed\n";
	print "copy of perl.\n\n";
	print "Currently, it is configured to be \"$command\", however,\n";
	print "that file either does not exist or is not a program.\n\n";
	print "Some common locations for Perl are:\n";
	print "  /usr/bin/perl\n";
	print "  /usr/local/bin/perl\n";
	print "  /opt/gnu/bin/perl\n\n";
        exit;
    }
}

# MakeCommon
#
# Make some common links to the counter

sub MakeCommon {
    local($force) = @_;
    local($ext);

    print "Installing the counter...\n";
    print "   ...making counter executable\n";
    chmod(0755,$0);

    local($path, $name, $cgi);
    $name = $0;
    if ($name =~ /^(.*\/)([^\/]+)$/) {
	$path = $1; $name = $2;
    }
    if ($name =~ /^(.*)(\.cgi)$/) {
	$name = $1, $cgi = $2;
    }

    foreach $ext (@CommonExtensions) {
	print  "   ...making link from $path$name$cgi to $path$name$ext$cgi\n";
	if (!&MakeLink("$path$name$cgi","$path$name$ext$cgi",$force)) {
	    # An error occured while making the link.  :-(

	    print "     *** An error occured while making the link.\n";
	}
    }
    if ($symlink_exists == 0 && $link_exists == 0) {
	print "* NOTE *  Your system does not support symbolic or hard links,\n";
        print "          copies made instead.  If you modify the counter, you must\n";
	print "          run counter -install again to recopy it to the other files.\n";
    }

    print "...done!\n";
}

# MakeLink
#
# Actually create the link.

sub MakeLink {
    local($oldname,$newname,$force) = @_;

    # Check to see if we can make symbolic links instead of hard links
    if (!defined $symlink_exists) {
	$symlink_exists = (eval 'symlink("","");', $@ eq '');
    }

    # Check to see if we can make a link if we can't make a symlink
    if (!symlink_exists) {
	$link_exists = (eval 'link("","");', $2 eq '');
    }

    if ($force) {
	# Check to see if the file exists
	if (-e $newname) {
	    if (!unlink ($newname)) {
		return 0;
	    }
	}
    }

    if ($symlink_exists) {
	return symlink($oldname, $newname);
    } elsif ($link_exists) {
	return link($oldname, $newname);
    } else {
	# Copy it the old-fashioned way...  *sigh*
	open(OLDFILE, $oldname) || die "Can't open $oldname for copy";
	open(NEWFILE, ">$newname") || die "Can't open $newname for write";
	while(<OLDFILE>) {
	    print NEWFILE $_;
	}
	close(NEWFILE);
	close(OLDFILE);
    }
}

####################################################################
#
# Ordinalizing functions
#

# ordinalize
#
# Call the appropriate ordinalize function for the default language

sub ordinalize
{
    local($count) = @_;

    if (defined $arg{'lang'}) {
	return eval("&ordinalize_$arg{lang}($count)");
    } else {
	return eval("&ordinalize_$default_lang($count)");
    }
}


# ordinalize_english
#
# Figure out what suffix (st, nd, rd, th) a number would have in ordinal
# form and return that extension.

sub ordinalize_english {
    local($count) = @_;
    local($last, $last2);

    $last2 = $count % 100;
    $last = $count % 10;

    if ($last2 < 10 || $last2 > 13) {
	return "st" if $last == 1;
	return "nd" if $last == 2;
	return "rd" if $last == 3;
    }

    return "th";		# Catch "eleventh, twelveth, thirteenth" etc.
}

# ordinalize_french
#
# Trivial...  Return the extension for french.  The only exception is 1.
# Thank you Chris Polewczuk <chris@hexonx.com>

sub ordinalize_french {
    local ($count) = @_;

    if ($count == 1) {
	return "'ière";
    } else {
	return "ième";
    }
}

# ordinalize_swedish
#
# A function to ordinalize in Swedish.  Thanks go to Johan Linde
# <jl@theophys.kth.se> for the code!

sub ordinalize_swedish {
    local($count) = @_;
    local($last, $last2);

    $last2 = $count % 100;
    $last = $count % 10;

    if ($last2 < 10 || $last2 > 12) {
        return ":a" if ($last == 1 || $last == 2);
    }

    return ":e";
}


########################################################################
#
# Output functions
#
# The following are the routines that actually convert the number
# of accesses into something that we print out.
#
# The name of each function is "output_" followed by the program's name.
# For instance, is the program is called "counter" then "output_counter"
# will be called; a program called "counterbanner" will call
# "output_counterbanner" to get the output.
#
# If the function is not defined, then "output_counter" will be called.
#

# output_counter
#
# The simplest function: just returns the number of accesses and the link.

sub output_counter {
    local($count) = @_;

    return &translate_output($count), $Link; # we return the count and the link
}


# output_counterord
#
# Return the number of accesses as an ordinal number.  (ie. 1st, 2nd, 3rd, 4th)

sub output_counterord {
    local($count) = @_;

    return &translate_output($count . &ordinalize($count)), $Link;
}


# output_counterbanner
#
# A somewhat silly one that uses the "banner" command to print out the
# count.  :)  You might need to change the path to make it work.

sub output_counterbanner {
    local($count) = @_;
    
    $banner = `banner $count`;

    return "<pre>$banner</pre>"; # return no link here (it would be annoying)
}


# output_counterfiglet
#
# An even sillier one than counterbanner.  :)

sub output_counterfiglet {
    local($count) = @_;

    $fig = "echo $count | /usr/games/figlet";	# setup command line
    $fig .= " -f $arg{'f'}" if $arg{"f"};	# use a different font?
    $fig = `$fig`;
    $fig =~ s!&!&amp;!;
    $fig =~ s!<!&lt;!;
    return "<br><pre>" . $fig . "</pre>";	# note no link here, either
}



#########################################################################
#
# Conversion functions
#

# UpdateVersion
#
# Convert a version 1file into a version 2 file.

sub UpdateVersion1 {
    local ($contents,$dummy);
    local ($oldsep) = $/;

    $/ = "";
    seek(COUNT,0,0);		# Go to the beginning of the file
    $contents = <COUNT>;
    seek(COUNT,0,0);
    print COUNT "$FileVersion\n";
    print COUNT $contents;
    seek(COUNT,0,0);
    $/ = $oldsep;
    $dummy = <COUNT>;		# Skip the new line
}


# ConvertDocV1
#
# Convert the a version 1 line into a version 2 line

sub ConvertDocV1 {
    local ($doc_uri,$old_uri,$accesses,$location) = @_;
    local ($contents,$dummy,$oldsep);

    $oldsep = $/;

    seek (COUNT,$location,0);	# Skip the line in question
    $dummy = <COUNT>;
    
    $/ = "";			# Read in the whole file
    $contents = <COUNT>;

    seek (COUNT,$location,0);
    
    local ($longaccesses,$hexflags);
    $longaccesses = sprintf("%010.10d", $accesses);
    $hexflags = sprintf("%04.4x", $flags);

    # Print out the new stuff
    print COUNT "'$doc_uri' $longaccesses $hexflags\n";
    print COUNT $contents;

    $/ = $oldsep;
}
