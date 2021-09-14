---
title: A reluctant ICSE submission cap post or, an exploration of primary sources
date: 2016-04-21
permalink: /posts/2016/04/post-1
tags: 
   - academia
   - icse
   - pc
   - reluctantrant
---

(Context: I was on the ICSE 2016 PC and I am on the ICSE 2017 PC.  I have never submitted more than three papers to ICSE.)

Much recent brouhaha in the software engineering research community on the new 3-submissions-per-any-individual-author cap imposed by the ICSE 2017 organizing committee.  I've been resisting wading into this, but the recent email sent by the PC chairs (for whom I sincerely have nothing but the absolute highest respect) to the the PC notably invites/welcomes respectful discussion on this and any other policy.  It also includes the following:
<blockquote>Some detractors have been vigorous in their opposition, but we can point out that the policy has both its justification and (mostly silent) supporters.</blockquote>
This sentence has been rattling around in my head. Honestly, I've been finding <a href="https://www.cs.cmu.edu/~ckaestne/icse17/">those noisy detractors</a> fairly convincing, though I'm fundamentally sympathetic to the plight of PC chairs in general. That said, I was bothered by the "silent supporters" and "existence of justification" claims absent further expansion.

There are various types of evidence that could be presented based on data from previous ICSEs that might convince me that the cap is a good solution to an important problem.[<a href="#icse1">1</a><a name="backtoicse1"></a>] For example, if this policy might cut the review load by a third, or if the majority of submissions receiving Cs or below came from bulk submissions, I <em>might</em> come around.

Reflecting on this, I thought, well, maybe that data <em>is</em> available. I wouldn't want to claim otherwise if I simply hadn't looked hard enough. The email to the PC, which I'm trying not to quote too liberally because even bulk emails are private correspondence, includes:
<blockquote>The potential problem of bulk submission to ICSE was first documented by the chairs of ICSE 2015, and the idea of limiting the number of submissions was then suggested as a potential solution. All this information is publicly available:
<a href="http://www.icse-conferences.org/sc/ICSE/2015/ICSE2015-Technical-Track-Report-Canfora-Elbaum.pdf">http://www.icse-conferences.org/sc/ICSE/2015/ICSE2015-Technical-Track-Report-Canfora-Elbaum.pdf</a>.</blockquote>
To the primary sources, then.  The basic claim is that the review load is increasing beyond the bounds of scalability and that this cap is important to improving either the quality of submissions or the sustainability of the ICSE review load. From the <a href="http://www.cs.mcgill.ca/~martin/blog/2016-04-15.html">blog post articulating the policy publicly</a>:
<blockquote>One of the main reasons for this policy is that every year more people submit more papers, but the pool of qualified reviewers willing to make the necessary commitment does not grow in proportion... We are stuck in a vicious cycle.</blockquote>
Long story short: it's not evident to me, based on the 2015 Technical Report (which details a system with an actual physical meeting, which should scale <em>less </em>well than 2016/2017's Program Board model), that we are in such a cycle.  Three bullets stand out from the Executive Summary:
<ul>
	<li>Page 2, under expertise and quality: "- Reviewing expertise was higher than previous ICSEs (as reported by authors and reviewers)"</li>
	<li>Page 2, under reviewing load: "-90% [of reviewers] agreed that the load and schedule was manageable"</li>
	<li>Page 3, under "Brief reflection from the chairs", which includes suggestions on what to "keep", "refine", "explore", or "drop": "Drop: Panic about scalability of reviewing process."</li>
</ul>
That is: The reviews were good, the load was manageable, and all the strum und drang about review process scalability is unwarranted.  These points are expanded in the document proper.  From Page 32, Section 4, Reflections from the Chairs (emphasis original):
<blockquote><strong>Balanced process.</strong> We believe that, given the number of submissions and its rate of growth, the reviewing model we used this year struck a good balance between maintaining a manageable load for reviewers...Note that simply adding more RC members to contribute reviews in the first phase would make the process scale further.</blockquote>
and
<blockquote><strong>No reason to panic about scalability of process.</strong> ...when considering the 452 submissions for this ICSE, the growth may be linear but with a very small coefficient. This clearly requires close monitoring in the future but no dire measures.</blockquote>
This sounds like we have/had a sustainable model that may be scaled by adding  a small number of committee members[<a href="#icse2">2</a><a name="backtoicse2"></a>] and shifting the load somewhat.[<a href="#icse3">3</a><a name="backtoicse3"></a>] It does not sound like a vicious cycle.

2015's chairs do propose an exploration on bounding the number of submissions per author. On page 35:
<blockquote><strong>Bounding the number of submissions per author.</strong> It may be worth exploring whether defining a maximum number of submissions per author would help to curb the abusive shotgun approach to submissions and encourage authors with multiple collaborations to submit just their best work...enforcing a limit of three submissions per author would reduce the number of submissions by approximately 8% and we conjecture that the program will not suffer.</blockquote>
That amounts to 1.44 fewer papers on average, for those of us reviewing the max of 18.  This is basically marginal. I have served on three PCs with review loads of 18+ (and several smaller venues) over the last 12 months.[<a href="#icse4">4</a><a name="backtoicse4"></a>]  I wouldn't complain about a reduction, but the difference between 18 and 17 does not determine whether I accept an invitation.

The final claim is that this policy will encourage authors to submit their best work.  But: 2015's chairs say that only 34 papers would have been blocked by the cap.  Even if they were all rejected, so were 334 others.  Table 3 outlines the score distribution: 220 submissions overall received only Cs or Ds. If we assume that <em>every single one </em>of those 34 papers is <em>terrible </em>(which the report authors do not), they could constitute no more than 15% of the terrible papers, leaving 186 other terrible papers to review. That's a third of a terrible paper less to review per PC member, which again is marginal (and represents a best case).  I'd bet that most terrible papers are submitted by authors on only one submission, simply based on the underlying distribution.

Somewhat on that subject, from Section 2.4:
<blockquote>The large number of submissions for some authors may be a reflection of an undesired and costly shotgun submission pattern, but it also seems to be associated with authors that carry many active collaborations. We have not enough data to tease this out further.</blockquote>
This section does <em>not</em> provide information of the number of submissions per co-author, nor the number of acceptances per bulk-submitting author. It does say that the <em>vast majority</em> of authors (their words, not mine) are only on one submission, which concerns me because it means that selecting down for prolific submitters will prevent submission outright for their collaborators.

tl;dr: Based on the 2015 report, which is the only ICSE- or even SE-specific document I've seen cited in this discussion, I do not see the strong motivation for a hard submission cap.  I'm interested to know if the 2016 data is notably different.  Adding overhead to bulk submission may be reasonable, and other venues have done this.  As a person who serves on multiple PCs, I<em> </em>like the idea of having authors who resubmit a paper include the previous reviews and a list of changes (...on the other hand, reviewing an <em>identical </em>paper a second time has the definite benefit of being easy...).

The PC chairs have stated that there is justification for this policy and have promised an FAQ on it.  I believe them, and if my opinion is worth anything, it would be wonderful  if that FAQ contains empirical evidence to substantiate that this policy will (A) be impactful in improving the quality of submissions/review experience, while (B) <em>not </em>harming the submission prospects of graduate students or other junior collaborators. The evidence cited so far is incomplete, but what it contains is not fully convincing on these points.

[<a name="icse1"></a>1] As part of our decision to implement double-blind review, my PC co-chair for SSBSE 2014 (a <em>much</em> <em>smaller</em> symposium, its worth mentioning; I'm not <em>at all</em> claiming it's equivalent to ICSE. Though I do think the latter should also do double-blind, FWIW) insisted we write a blog post justifying the decision. My first reaction was "...uh, because we're the PC chairs and we said so?" But I did it, because Shin was right.  My opinion on double-blind review is informed by the substantive body of work in implicit bias in general and the study of academic double blind review in particular, and <a href="http://clairelegoues.com/double-blind-review-at-ssbse/">I highlighted some of that literature in the post</a>. I don't believe we convinced everyone, but I do know anecdotally that members of the community appreciated our data-driven approach to conference organization decision making.<a href="#backtoicse1">^</a>

[<a name="icse2"></a>2] This year's chairs mention that it is difficult to fill a PC.  2015's chairs speak favorably of the benefits of recruiting and cultivating junior community members (like myself, which I greatly appreciate, bloviating blog posts notwithstanding), mentioning that "This is, in our opinion, a key way to educate future leaders in the ICSE community and, as such, it has a great value for the community."<a href="#backtoicse2">^</a>

[<a name="icse3"></a>3] I do like a two-phase review system. I reviewed the same number of papers for ISSTA as I did for ICSE in 2016, but in two phases, and it felt much more manageable.<a href="#backtoicse3">^</a>

[<a name="icse4"></a>4] I review a lot.  I'm learning to say no.  It's a process.<a href="#backtoicse4">^</a>

<em>Opinions my own, not my employers', etc etc.</em>