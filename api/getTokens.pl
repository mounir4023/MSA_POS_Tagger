################################################################################
# getTokens.pl
# Fatma Nasser Al Shamsi
# (c) 2005 ,  the University of Sharjah
################################################################################
# This program is free software;
# usage:
# perl -w getTokens.pl <infile.txt> TokensOut.txt
# were "infile" is the input text in Arabic Windows encoding
# and "TokensOut" is the output token list
################################################################################
#
# Acknowledgment : Many thanks to Mr.Tim Buckwalter from QAMUS LLC (www.qamus.org),
# for sharing with us his stemmer lexicon and code.
#
################################################################################




while (<STDIN>) {

    print STDERR "reading input line $.\r";
   @tokens =  tokenize($_); # returns a list of tokens (one line at a time)

   foreach $token (@tokens) {
                  print "$token \n";

            }

}

# ============================
sub tokenize {

   $line = shift @_;
   chomp($line);
   $line =~ s/^\s+//; $line =~ s/\s+$//; $line =~ s/\s+/ /g; # remove white space
   @tokens = split (/([^\x81\x8D\x8E\x90\xC1-\xD6\xD8-\xDF\xE1\xE3-\xE6\xEC-\xED\xF0-\xF3\xF5\xF6\xF8\xFA]+)/,$line);
   return @tokens;

}