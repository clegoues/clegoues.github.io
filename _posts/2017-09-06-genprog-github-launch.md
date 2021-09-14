---
title: My original PWLConf reading list on patch generation
date: 2017-09-06
permalink: /posts/2017/09/post-1
tags: 
   - programrepair
---
My collaborators and I started GenProg, "[Genetic|Generic] Program Repair (Depending on Whom You Ask)", in 2008, maybe a month or so after GitHub was launched.  My grad school research group was hip and up-to-date in our development tools, primarily evidenced by the fact that we used Subversion instead of CVS.  Even in 2011, when we started putting together what became the <a href="http://repairbenchmarks.cs.umass.edu">ManyBugs dataset</a>, it was still completely reasonable to find open source projects to study by trolling <a href="http://www.sourceforge.net">Sourceforge</a>. Which is exactly what we did.

Similarly, at the time, it was basically reasonable to release data, code, and reproduction instructions by calling svn export on the repo and tarballing everything up and linking to it from a website.  Which is also exactly what we did.

But: it's 2017, for Crying Out Loud.  That approach is now so unreasonable that new students look at me incredulously when I tell them about it.  <em>They think I'm kidding. </em>This motivated one of my summer projects, to drag a long-existing project into the modern era.

Behold:
<ul>
	<li><a href="https://squareslab.github.io/genprog-code/">https://squareslab.github.io/genprog-code/</a> is the new website for GenProg-related projects/publications/etc. Expect updates as we continue pull in more results/datasets from the various groups into the one place (#catherding).</li>
	<li><a href="https://github.com/squareslab/genprog-code">https://github.com/squareslab/genprog-code</a> is a public github repository, converted from the private svn repo that supported much of the GenProg-related development from roughly 2010 (earlier sources are linked, but without history).</li>
</ul>
Caveat: The quotations around "GenProg" are deliberate.  To the best of my knowledge[1], most recent extensions of that codebase use it as a jumping off point for new evolutionary/genetic improvement techniques for non-functional properties (rather than new approaches for bug repair per se). The work on graphics shaders is particularly cool, IMO, which I can say freely because I have literally nothing to do with it.

All that to say: the codebase has a long and meandering history.  We're doing our best to organize the materials coherently, but it's a work in progress, and the job of rendering it accessible is complicated by the multiple collaborators and projects involved, and the (temporal) length of that collaboration.  Please be kind.  Please also feel free to file issues, issue pull requests, send mail, or otherwise complain and make suggestions to help make it (site, code, etc) better.

[1] I confess I personally haven't really made many substantive commits in, well, years (I've given access to a private fork to students for work that evaluates/builds on it; still working on folding that stuff in to the new site).  Yes, it's been a while since I graduated, and this shouldn't have taken so long, but it turns out that the tenure track is time consuming and old habits go down hard.
