---
title: My original PWLConf reading list on patch generation
date: 2016-09-16
permalink: /posts/2016/09/post-1
tags: 
   - programrepair
   - pwlconf
---

I loved speaking at the inaugural <a href="http://pwlconf.org">Papers We Love conference</a>, co-located with <a href="http://thestrangeloop.com">Strange Loop</a>, in the disarmingly cool city of St. Louis. I'd never been to or spoken at a <a href="http://paperswelove.org">PWL event</a> before, but I've had a great time getting to know the community. The basic idea is a bunch of &nbsp;meetups where participants (a mix of industry and academic types) present/discuss academic papers that they, well, love.&nbsp;

I of course violated the ethos by speaking in part about my own work in the context of an introduction to patch generation research. Whoops. In my defense, I sang the praises of not-my-work when I discussed recent results from Sergey Mechtaev, Jooyong Yi, and Abhik Roychoudhury (all from the National University of Singapore) on <a href="http://angelix.io">Angelix, new technique for multiline semantic program repair</a>&nbsp;(a paper that I do, indeed, love).

Anyway. When I was first asked for which papers I would touch on in my talk, I was like HMMMMMM what is the ESSENTIAL reading list for a person who has no former exposure to this area and yet wants to learn ALL OF THE THINGS I MIGHT EVER TALK ABOUT. And so I produced a 10.5- item bibliography (that left a lot out!). Brevity: Not My Thing.

The organizers gently suggested that I slow my roll, and so I cut it down to the 2.5 papers I actually discussed in any detail, though I did touch on the work in many others. I've been asked to post the more extensive list, so here we are.&nbsp;

Caveats: <a href="http://automated-program-repair.org">automated-program-repair.org</a> tracks work in automated program repair, is kept up to date, and is significantly more complete than my list. My list was constructed at a particular moment in time to support a particular type of talk on source-level patch generation for bug repair (ignoring dynamic/web languages and contract-based repair entirely); it thus should not be treated as the gospel word on "the Important Papers in Program Repair." Instead, think of them as "the papers Claire pointed to as a reasonable overview that fit well within the context of a talk she gave on the subject." That is: If I left your favorite paper out its not because I think it's not important.

Finally: if you like this stuff, consider grad school. And check the box next to <a href="http://www.isri.cmu.edu/education/se-phd/index.html">PhD in Software Engineering</a> when you <a href="https://www.scs.cmu.edu/doctoral-admissions">apply to CMU</a>.

Reading strategies: As context, patch generation is generally conceptually divided into "heuristic" strategies and "semantic" strategies, but there is a general sentiment in the community that they are beginning to merge. The challenges in the space traditionally break down into scalability, output quality (are the patches good?), and expressive power.

<i>Based on interest: if a reader wants...</i>
<ul>
	<li>...to read a SINGLE paper to get the flavor, read (1), which overviews one of the first salvos in heuristic repair on a relatively accessible way. If she plans to read anything else, it's probably not worth the trouble.</li>
	<li>...a more comprehensive picture of heuristic repair, read (2) and/or (3) (2 gives a complete story; 3 is more recent and has cooler experiments) and then at least (6) (and 6a, if she's feeling completist). If the reader is on a tear she should read (7), too, especially if she cares about Java.</li>
	<li>...an introduction to semantic repair, read at least (5), and possibly (4). If both are read, read (4) first. I included (4) at least in part because it has a really beautiful background section on the synthesis technique that underlies the family of approaches, so it may be worth referencing that background section while reading (5) instead of reading them both. They link other papers in this line of work <a href="http://angelix.io">at their website</a>.&nbsp;</li>
	<li>...human-rated assessments of patch quality, read (7), and/or (8). &nbsp;&nbsp;</li>
	<li>...to know about using human patches to inform the construction of patches, read (6) and (7). Possibly in the other order. . There's more like this, especially recently, but I'm trying (and failing) to be selective!</li>
	<li>....to know about the in the ways semantic and heuristic approaches are starting to come together, read (9) and maybe also (5). The evaluation in (9) is based on the work in (10), which may not be quite worth reading on its own for this hypothetical reader but as I included some results from it, I thought it worthwhile to list. &nbsp;</li>
</ul>
<i>Based on number of papers to read (these suggestions shouldn't be taken as gospel, but I did my best to make it sensible):</i>
<ol>
	<li>(1)</li>
	<li>(2) or (3), (5)</li>
	<li>(2) or (3), (5), (7)</li>
	<li>(2) or (3), (5), (7), (9)</li>
	<li>(2) or (3), (5), (7), (6), (9)</li>
	<li>(2) or (3), (5), (7), (6), (9), (8)</li>
	<li>(2) or (3), (4), (5), (7), (6), (9), (8)</li>
	<li>(2) or (3), (4), (5), (7), (6), (9), (8), (10)</li>
</ol>
<i>Papers (I'll add links when I'm not on my iPad!):&nbsp;</i>
<ol>
	<li>Westley Weimer, Stephanie Forrest, Claire Le Goues and ThanhVu Nguyen. Automatic Program Repair with Evolutionary Computation Communications of the ACM (CACM) Vol. 53 No. 5, May, 2010, pp. 109-116.</li>
	<li>Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest and Westley Weimer. GenProg: A Generic Method for Automated Software Repair. IEEE Transactions on Software Engineering (TSE) 38(1): 54-72 (January/February 2012)</li>
	<li>Claire Le Goues, Michael Dewey-Vogt, Stephanie Forrest and Westley Weimer.A Systematic Study of Automated Program Repair: Fixing 55 out of 105 bugs for $8 Each. International Conference on Software Engineering (ICSE), 2012: 3-13.</li>
	<li>Hoang Duong Thien Nguyen, Dawei Qi, Abhik Roychoudhury, and Satish Chandra. SemFix: program repair via semantic analysis. International Conference on Software Engineering (ICSE), 2013: 772-781.</li>
	<li>Sergey Mechtaev, Jooyong Yi, and Abhik Roychoudhury. Angelix: scalable multiline program patch synthesis via symbolic analysis. International Conference on Software Engineering (ICSE), 2016: 691-701.</li>
	<li>Fan Long and Martin Rinard. Automatic patch generation by learning correct code. Principles of Programming Languages (POPL), 298-312.
(This builds on (6a) Fan Long and Martin Rinard. Staged program repair with condition synthesis. Joint Meeting on Foundations of Software Engineering (ESEC/FSE), 2015: 166-178. ...Which is also what the Angelix paper compares to, so if you're feeling adventurous/completist, you might read both.)</li>
	<li>Dongsun Kim, Jaechang Nam, Jaewoo Song, and Sunghun Kim. 2013. Automatic patch generation learned from human-written patches. International Conference on Software Engineering (ICSE), 2013: 802-811.</li>
	<li>Zachary P. Fry, Bryan Landau, Westley Weimer: A Human Study of Patch Maintainability. International Symposium on Software Testing and Analysis (ISSTA), 2012: 177-18.</li>
	<li>Yalin Ke, Kathryn T. Stolee, Claire Le Goues, and Yuriy Brun. Repairing Programs with Semantic Code Search. In Automated Software Engineering (ASE), 2015: 532-543.</li>
	<li>Edward K. Smith, Earl Barr, Claire Le Goues, and Yuriy Brun, Is the Cure Worse than the Disease? Overfitting in Automated Program Repair. Joint Meeting of the European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE), 2015: 532–543.</li>
</ol>