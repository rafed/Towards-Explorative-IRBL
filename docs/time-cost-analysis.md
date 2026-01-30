## Cost
Apart from higher accuracy, GenLoc is also cost-effective. The average cost to localize a bug in Ye et al. dataset, GHRB dataset and SWE-bench Lite is \$0.010, \$0.025 and \$0.023 respectively. The lower per-bug cost on the Ye et al. projects, despite their larger size in terms of files and lines of code, arises from their multi-version structure: once the initial embedding is completed, only changed or newly added files need to be reprocessed in later versions. By contrast, GHRB and SWE-bench Lite include more projects but far fewer bug reports per project, so a larger fraction of projects must go through the full initial embedding stage without enough subsequent bugs to offset this overhead. Nevertheless, the per-bug cost remains reasonable, demonstrating that GenLoc is affordable and practical for both long-lived projects and newer projects with fewer versions. Moreover, unlike BugLocator [1], BRTracer [2] and DreamLoc [3], GenLoc relies solely on the bug report, thereby making it broadly applicable even in projects without historical bug-fix data. 

---

## Time

On average, GenLoc takes 47.7 seconds to process one bug. This is consistent with findings from a prior practitioner study [4], which reported that 90\% of developers expect a bug localization technique to return results within one minute. This suggests that GenLoc can operate within developer-expected timeframes while maintaining high accuracy and low cost, highlighting its suitability for real-world debugging scenarios.

---

## References

[1] Zhou, J., Zhang, H., & Lo, D. (2012, June). Where should the bugs be fixed? more accurate information retrieval-based bug localization based on bug reports. In 2012 34th International conference on software engineering (ICSE) (pp. 14-24). IEEE.

[2] Wong, C. P., Xiong, Y., Zhang, H., Hao, D., Zhang, L., & Mei, H. (2014, September). Boosting bug-report-oriented fault localization with segmentation and stack-trace analysis. In 2014 IEEE international conference on software maintenance and evolution (pp. 181-190). IEEE.

[3] Qi, B., Sun, H., Yuan, W., Zhang, H., & Meng, X. (2021). Dreamloc: A deep relevance matching-based framework for bug localization. IEEE Transactions on Reliability, 71(1), 235-249.

[4] Kochhar, P. S., Xia, X., Lo, D., & Li, S. (2016, July). Practitioners' expectations on automated fault localization. In Proceedings of the 25th international symposium on software testing and analysis (pp. 165-176).