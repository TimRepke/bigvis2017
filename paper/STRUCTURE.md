# Related Work

## Related Research Areas
- Exploratory Search
- Visual Search
- Clustering, Language Models, Network Metrics

## Literature Overview
- [2] Extract topics and derive time-sensitive keywords to depict the content evolution of each topic over time visualised as stacked plots 
  - Dataset: personal emails (8k) and emergancy room data (23k patient records)
  - Dimensions: Time, Topics (and derived Keywords)
- [3] Select representative samples before visualisation to reduce visual noise by embedding
  - Dataset: 20 Newsgroups, 10PubMed
  - Dimensions: Groups or Deseases, Documents by TopicModel in 2D space
- [4] ...
- [5] Visualisation System for thematic maps that position Concepts (ie Named Entities) into semantic space on map
  - Dataset: Wikipedia,  Wikidata
  - Dimensions: Entities (Films, Bands/Musicians, Companies), Category (Genre, Company), Topic Cluster (Document Embedding)
  - Implementation: [L4, L5]

# System Objective
- Document Exploration
- Knowledge Discovery
- Network Analysis
  - Understand (social) context of a person
  - Discover latent structures
  - ...
  
## Dimensions in our Domain
- People (extracted from email headers [name and address])
- Groups of people derived from domain in email address
- salient structures in communication network
- Named Entities mentioned in text
- Clusters of Document Embeddings
- Topics 
- Salient phrases / Keywords
- Time (ie abstracted to timeboxes, either dynamic length by number of mails or [variable] fixed length)

# References

- [1] Ryen W. White, Resa A. Roth. Exploratory Search: Beyond the Query-Response Paradigm. 2009 (http://www.morganclaypool.com/doi/abs/10.2200/S00174ED1V01Y200901ICR003)
- [2] Furu Wei, et.al. TIARA: A Visual Exploratory Text Analytic System. 2010, KDD (https://pdfs.semanticscholar.org/92c2/8f3df8fc20fbd56716886b04c31aafb3b37d.pdf)
- [3] Yanhua Chen, Lijun Wang, Ming Dong, Jing Hua. Exemplar-based Visualization of Large Document Corpus. 2009, TransVis (http://www.cs.wayne.edu/~mdong/tvcg09.pdf)
- [4] Martin Gronemann, Michael Jünger. Drawing Clustered Graphs as Topographic Maps. 2013, LNCS (https://link.springer.com/content/pdf/10.1007%2F978-3-642-36763-2_38.pdf)
- [5] Bret Jackson, Brent Hecht. Cartograph: Unlocking Thematic Cartography Through Semantic Enhancement. 2017, IUI (http://brenthecht.com/publications/iui_cartograph.pdf)

# Links
- [L1] Graph Drawing E-print Archive (http://gdea.informatik.uni-koeln.de/)
- [L2] Email Network as map (http://informatik.uni-koeln.de/public/graphmap/gdnet/web/index.php)
- [L3] Text Vis Paper overview (http://textvis.lnu.se/)
- [L4] Cartograph: Creates interactive maps from datasets (https://github.com/shilad/cartograph/)
- [L5] map of wikipedia -> cartograph (http://nokomis.macalester.edu/wmf_en/static/index.html)
- [L6] Advanced desktop search/corpus exploration prototype (https://github.com/mitre/rhapsode)

