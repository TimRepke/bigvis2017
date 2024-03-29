# Related Work

## Related Research Areas
- Exploratory Search
- Visual Search
- Clustering, Language Models, Network Metrics

## Literature Overview
- [1] 
- [2] Extract topics and derive time-sensitive keywords to depict the content evolution of each topic over time visualised as stacked plots 
  - Dataset: personal emails (8k) and emergancy room data (23k patient records)
  - Dimensions: Time, Topics (and derived Keywords)
- [3] Select representative samples before visualisation to reduce visual noise by embedding
  - Dataset: 20 Newsgroups, 10PubMed
  - Dimensions: Groups or Deseases, Documents by TopicModel in 2D space
- [4] 
- [5] Visualisation System for thematic maps that position Concepts (ie Named Entities) into semantic space on map
  - Dataset: Wikipedia,  Wikidata
  - Dimensions: Entities (Films, Bands/Musicians, Companies), Category (Genre, Company), Topic Cluster (Document Embedding)
  - Implementation: [L4, L5]
- [7] extract "concepts" through LSI (?) and render it
  - Dataset: descriptions of European Research Projects (6FP)
  - Dimensions: "concepts" in semantic space
  - TF*IDF BOW -> LSI -> "concept" = vector in resulting space -> multidimensional scaling (euclidian distance) to 2D
  - map is point density, keywords are TFIDF dominant in a square, crosses on map are embedded documents
- [8] higher order visualisation of network by adding (splitting) nodes to encode higher-order dependencies (ie conditional probability)
  - Dataset: Global shipping data (3.5mio voyages by 65k ships, 4k ports, 1yr)
  - Objective: (ie) discover ports relevant for species invasion
  - extract higher order dependencies (ie not pairwise, but tuple of len 3 -> cond prob of last node given first node)
- [9] CS map
  - Dataset:
  - Dimensions: Titles of papers (cities on map), word/phrase similarity (countries - cooccurence), conference/group/person profile (heatmap)
  - basemap can be fixed, heatmap for time intervals -> see change over time
- [10] visualise hierarchical data as tree
- [11] cactus
- [12] Algorithm to layout a graph and regions, where nodes have classes, so that the nodes are within continuous regions
- [13] aggregates nodes based on their spatial distribution, thereby allowing for visual exploration of large graphs, contour lines/heatmap

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
- Emails
- Time (ie abstracted to timeboxes, either dynamic length by number of mails or [variable] fixed length)
  - detect evolving clusters/patterns
  - find interval of stable connectivity patterns (nothing changes) -> from there find periods of change (vs fixed time intervals)
  
## Ways to display dimensions
- time (resource allocation?)
  - slider
  - heatmaps
  - depth
  - intensity
  - path
- topics (what is the corpus about?)
  - areas
  - heatmaps
- people (criminal networks?)
  - nodes
  - stacked objects (including time or topics)
- emails (influence, information diffusion)
  - edges/paths
  - dots along a path
  - embedding
 

## Concepts
- Time, People, Topics, emails
  - time vertical
  - people horizontal as small circles
  - topics vertical at top (color gradient)
  - people emit glowing dots (emails) that rise in glowing paths to top
  - path contains all mails over time, intensity is frequency
  - find "good" order of people may be complicated (relevant to reduce overlapping paths)
  - tf/idf like score to filter topics, that are in all mailboxes to reduce noise
  - optional: south of that, show connections between people
- Time, People, Embedding/Topic, emails
  - analogy: person brick wall in perspective, seeing front
  - front: current time slice, bricks (intensity) reflect topic intensity
  - side of wall may show patterns (time = length of wall)
  - draw funnels between people indicating their connection and overlapping topic
  - time slider to skip though time (chaning connections)
  - layout, such that globally closeby people (network connectivity) are close, secondary topic
- people, embeddings, connections (inspired by [4,5])
  - recursively remove edges with least connections, each time a part disconnects, it becomes a level in hierarchical cluster
  - depth of leafs defines overall closeness between people
  - at some level in the hierarchical cluster, group people in one cluster
    - zoom defines which people are shown (either most connected or general popularity)
  - embed mails of those people, arrange people accoring to similarity of mails in area
  - arrange areas, such that overlapping topics meet at border
  - draw high level connections implied by the cluster tree
    - zoom defines level of detail (which lines are shown)
  - span virtual grid over map, for each cell, pick relevant words from corresponding documents in the cell and show them
    - grid size adapts to zoom
  - maybe time as (slider)
    - heatmap of activity in area
    - opacity of connection lines
    - opacity or heatmap of "topics"
- water level analogy for map models with depth metric/topology


# References

- [1] Ryen W. White, Resa A. Roth. Exploratory Search: Beyond the Query-Response Paradigm. 2009 (http://www.morganclaypool.com/doi/abs/10.2200/S00174ED1V01Y200901ICR003)
- [2] Furu Wei, et.al. TIARA: A Visual Exploratory Text Analytic System. 2010, KDD (https://pdfs.semanticscholar.org/92c2/8f3df8fc20fbd56716886b04c31aafb3b37d.pdf)
- [3] Yanhua Chen, Lijun Wang, Ming Dong, Jing Hua. Exemplar-based Visualization of Large Document Corpus. 2009, TransVis (http://www.cs.wayne.edu/~mdong/tvcg09.pdf)
- [4] Martin Gronemann, Michael Jünger. Drawing Clustered Graphs as Topographic Maps. 2013, LNCS (https://link.springer.com/content/pdf/10.1007%2F978-3-642-36763-2_38.pdf)
- [5] Bret Jackson, Brent Hecht. Cartograph: Unlocking Thematic Cartography Through Semantic Enhancement. 2017, IUI (http://brenthecht.com/publications/iui_cartograph.pdf)
- [6] Patrick Cheong-Iao Panga, Robert P. Biuk-Aghai, Muye Yang, Bin Pang. Creating realistic map-like visualisations: Results from user studies. 2017, VLC (https://sci-hub.bz/https://doi.org/10.1016/j.jvlc.2017.09.002)
- [7] Blaž Fortuna, Marko Grobelnik, Dunja Mladenić. Visualization of Text Document Corpus. 2005, Informatica (http://wen.ijs.si/ojs-2.4.3/index.php/informatica/article/viewFile/67/59)
- [8] Jun Tao, Jian Xu, Chaoli Wang, Nitesh V. Chawla. HoNVis: Visualizing and Exploring Higher-Order Networks. 2017 (https://arxiv.org/pdf/1702.00737.pdf)
- [9] Daniel Fried, Stephen G. Kobourov. Maps of Computer Science. 2014, PacificVis (https://arxiv.org/pdf/1304.2681.pdf)
- [10] Arnaud Sallaberry, Yang-chih Fu, Hwai-Chung Ho, Kwan-Liu Ma. Contact Trees: Network Visualization beyond Nodes and Edges. 2016, PLoS ONE (http://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0146368&type=printable)
- [11] Tommy Dang, Angus Forbes. CactusTree: A Tree Drawing Approach for Hierarchical Edge Bundling. 2017, PacificVis (https://creativecoding.soe.ucsc.edu/pdfs/Dang_CactusTree_PacificVis_2017.pdf)
- [12] Alon Efrat, Yifan Hu, Stephen G. Kobourov, Sergey Pupyrev. MapSets: Visualizing Embedded and Clustered Graphs. 2015, JGAA (http://www.emis.ams.org/journals/JGAA/accepted/recent/EfratHuKobourovPupyrev.pdf)
- [13] Jand Hildenbrand, Arlind Nocaj, Ulrik Brandes. Flexible Level-of-Detail Rendering for Large Graphs. 2016, GDNV (https://kops.uni-konstanz.de/bitstream/handle/123456789/36654/Hildenbrand_0-386032.pdf?sequence=1&isAllowed=y)

# Links
- [L1] Graph Drawing E-print Archive (http://gdea.informatik.uni-koeln.de/)
- [L2] Email Network as map (http://informatik.uni-koeln.de/public/graphmap/gdnet/web/index.php)
- [L3] Text Vis Paper overview (http://textvis.lnu.se/)
- [L4] Cartograph: Creates interactive maps from datasets (https://github.com/shilad/cartograph/)
- [L5] map of wikipedia -> cartograph (http://nokomis.macalester.edu/wmf_en/static/index.html)
- [L6] Advanced desktop search/corpus exploration prototype (https://github.com/mitre/rhapsode)
- [L7] Visual Bibliography of Tree Visualization (http://treevis.net/)
- [L8] CactusTrees: Visualizing Structure and Connectivityin Hierarchical Datasets (http://cactustrees.github.io/)
- [L8] Twitter impact over USA, zoom in to see streets (https://convergencela.com/)

