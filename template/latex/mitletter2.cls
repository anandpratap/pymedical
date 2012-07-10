\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mitletter2}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{letter}}
\ProcessOptions
\LoadClass{letter}
\usepackage[dvips]{graphics}
\usepackage[businessenvelope]{envlab}

\raggedright
\setlength{\topmargin}{-.80in}
\setlength{\oddsidemargin}{-.25in}
\setlength{\evensidemargin}{-.25in}
\setlength{\textwidth}{7in}
\setlength{\textheight}{8in}
\setlength{\headsep}{1in}
\setlength{\footskip}{1.625in}



\DeclareFixedFont{\boldfont}{OT1}{cmss}{bx}{n}{8}
\DeclareFixedFont{\regularfont}{OT1}{cmr}{m}{n}{8}
\DeclareFixedFont{\italicfont}{OT1}{cmr}{m}{it}{10}
\DeclareFixedFont{\IDfont}{OT1}{cmr}{m}{it}{8}


\newcommand{\officename}{Your Office Name}
\newcommand{\roomnumber}{X00-000}
\newcommand{\phonenum}{617.000.0000}
\newcommand{\faxnum}{617.000.0000}
\newcommand{\website}{web.mit.edu/abcdefghijk}
\newcommand{\email}{user@mit.edu}
\newcommand{\person}{Your name}
\newcommand{\ID}{Your title}

\renewcommand*{\opening}[1]{\ifx\@empty\fromaddress
  \thispagestyle{firstpage}%
    {\raggedleft\@date\par}%
  \else  % home address
    \thispagestyle{empty}%
    {\raggedleft\begin{tabular}{l@{}}\ignorespaces
      \fromaddress \\*[2\parskip]%
      \@date \end{tabular}\par}%
  \fi
  \vspace{2\parskip}%
  {\raggedright \toname \\ \toaddress \par}%
  \vspace{2\parskip}%
  #1\marginpar[\hfill test]\par\nobreak}
\renewcommand{\ps@headings}{% 
  \let\@oddfoot\@empty\let\@evenfoot\@empty
      \def\@oddhead{\slshape\headtoname{} \ignorespaces\toname
                    \@date
                    \hfil \pagename{} \thepage}%
      \let\@evenhead\@oddhead}
\renewcommand*{\opening}[1]{\ifx\@empty\fromaddress
  \thispagestyle{firstpage}%
    \@date\\%
  \else  % home address
    \thispagestyle{empty}%
    {\raggedleft\begin{tabular}{l@{}}\ignorespaces
      \fromaddress \\*[2\parskip]%
      \@date \end{tabular}\par}%
  \fi
  \vspace{2\parskip}%
  {\raggedright \toname \\ \toaddress \par}%
  \vspace{2\parskip}%
  #1\par\nobreak}
\renewcommand*{\signature}[1]{\def\fromsig{\italicfont #1}}


\newsavebox{\MassInstTech}
\newsavebox{\place}
\newsavebox{\mainaddress}
\newsavebox{\contactinfo}

\sbox{\MassInstTech}
     {\parbox[b]{160mm}
       {\setlength{\baselineskip}{9.2pt}\begin{center}\scalebox{.4}{\includegraphics*{mitlogo.eps}}\\[9.2pt]\boldfont{Massachusetts Institute of Technology}\\\vspace{9.2pt}\regularfont{\person}\\\IDfont{\ID}\end{center}}}

\sbox{\place}
     {\parbox[t]{7.29cm}
       {\setlength{\baselineskip}{9.2pt}{\boldfont Office name} \\ {\regularfont Building X00-000}}}

\sbox{\contactinfo}
     {\parbox[t]{3.59cm}
       {\setlength{\baselineskip}{9.2pt}\regularfont{Phone\hspace{4mm}    \phonenum\\
	   Fax\hspace{7.5mm}      \faxnum\\
	   Email \hspace{3.6mm} \email\\
	   \website}}}

\sbox{\mainaddress}
     {\parbox[t]{4.13cm}
       {\setlength{\baselineskip}{9.2pt}\regularfont{77 Massachusetts Avenue\\
	   Cambridge, Massachusetts\\
	   02139-4307}}}
	   

\newsavebox{\footer}
%put it all together
\sbox{\footer}
     {\raisebox{1cm}{\parbox[t]{16.51cm}
       {\hspace{.25in}\usebox{\place} \usebox{\mainaddress} \usebox{\contactinfo}}}}

\newsavebox{\envelope}
\sbox{\envelope}
     {\parbox[t]{6cm}{\setlength{\baselineskip}{9.2pt}\boldfont{\officename}\\\\\\\hspace*{.5in}\scalebox{.25}{\includegraphics*{mitlogo.eps}}\\\\\boldfont{Massachusetts Institute of Technology}\\\regularfont{77 Massachusetts Avenue, Building \roomnumber}\\\regularfont{Cambridge, MA 02139-4307}}}

\renewcommand{\returnaddress}{\protect\usebox{\envelope}}

%make sure the header goes on the first page
\renewcommand{\ps@firstpage}
	     {\setlength{\headheight}{3cm}\setlength{\headsep}{1cm}%
	       \renewcommand{\@oddhead}{\usebox{\MassInstTech}}%
	       \renewcommand{\@oddfoot}{\raisebox{55pt}[0pt]{\usebox{\footer}}}}

\providecommand{\@evenhead}{}\providecommand{\@oddhead}{}
\providecommand{\@evenfoot}{}\providecommand{\@oddfoot}{}

\pagestyle{headings}
