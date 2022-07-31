select * from "TranslationSentences" ts where sentence = ''
select * from "TranslationSentences" ts where sentence is null


select * from "TranslationSentences" ts where "sourceSentence"  = ''
select * from "TranslationSentences" ts where "sourceSentence" is null 
select * from "TranslationWorks" tw 

select count(*) from "TranslationSentences" ts 

select * from "TranslationSentences" ts  where "sourceSentence"  ='D'
select * from "TranslationSentences" ts  where length("sourceSentence") < 2

