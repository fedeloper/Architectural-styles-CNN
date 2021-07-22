FDS Report - Architectural styles CNN

Michael Cozzolino

cozzolino.1928667@studenti.uniroma1.it

Mattia Capparella

capparella.1746513@studenti.uniroma1.it

Federico Fontana

fontana.1744946@studenti.uniroma1.it

Abstract to 10.000 images ( 5000 new images have been scraped automatically from Google). No custom

Thementationaim ofofthisan Architecturalproject consistsStylein theClassifierimple-, models have been created: he experimented on

improving the results published in Zhe Xu’s both resnet34 and resnet50, obtaining better results paper, and disproving the results obtained by on the latter. Our firstassumption of biased results

Marian Dimitru’s solution posted on Kaggle. due to a bad augmentation process turned out to Our results show that data preparation gener- be apparently wrong: there are some discrepancies ally improves the performance, but the choice between the description of what has been done and

of a deeper network might outperform alone the code itself on Dumitru’s GitHub page that let even composite and more complex approach. us think no strange input manipulation occurred

1 Problem overview and the boosted performance are a consequence of the dataset enlargement.

Themaintaskistodistinguishanarchitecturalstyle

from another. The presence of mutual influences 3 Proposed method explained

among styles, re-interpretation, revival and so on,

can easily lead to low inter-class variations, making 3.1 Preprocessing

this kind of classificationa particular one. This is the firstcontribution of our work: we intro-

duce an offline preprocessing algorithm to refine 2 Related work training and test data. Even if the images gathered

1. Original paper by Xu are in general good quality photos, yet they present some noise and other elements of disturb

Xu’s solution consists in adopting a Deformable that could degrade both training and testing phase. Part-based Models (DPM) to detect the position The algorithm can be summarized in 4 main steps: of a facade in the image while capturing the mor-

phological characteristics of each style, sided by 3.1.1 Image Denoising

Multinomial Latent Logistic Regression (MLLR) We use a Non-local Means denoising algorithm as the learning algorithm to carry out the classifi- with a dual purpose: first to achieve much greater cation with probabilistic analysis. DPM models post-filteringclarity while preserving more details both global and local features enabling a flexible intheimage(wrtlocalmeanalgorithm)andsecond configurationof local patches introducing some de- toreducethecolorpaletteofsimilarhues: scanning formation costs, while the introduction of MLLR wider portions of the image while computing the enables soft assignment results and simultaneous average values for similar pixels, we start the con- training phases for all the classes classifiers. To vergence of slightly different colors into a single tackle this task, neither a ad hoc pre-processing one.

step nor the canonical augmentation techniques

have been performed on the dataset. 3.1.2 Conversion into HSV colorspace

We do convert the images into the HSV color space

2. Dimitru’s variation as a standard procedure in image analysis: when Dimitru proposes a slight paradigm shift: he adopts dealing with image segmentation, having a color

a convolutional neural networkto perform the clas- space whose elements are as independent as possi- sificationtask. The original dataset is enlarged up ble is a great advantage, and separating a color in

hue, lightness and saturation is the most effective 3.2 Data Augmentation Online

procedure. The benefit we derive from this oper- This technique helps us to increase dataset vari- ation comes from the fact the hue component of ability and avoid overfitting. The transformations same or similar colors will be very close, regard- we are introducing are normal photo noises like less external effects such as bright lights, shadows, rotation, cropping, changing in brightness, contrast, reflectionsand so on. tonality. Our focus was in Erasing random zones

3. Color Extraction on images, we notice helps the model to get better performance in the test dataset avoiding some local

weOncecandefinedcomputethetherangesmasksof theof thesehuescolorsto be remoand sub-ved, minima. For image data, online augmentation is

motivated by observing that we can translate or add tractonce thisthemoperationfrom theis doneoriginalis animage.image inWhat’whichs leftthe noise or otherwise distort an image but retain its

sky and greenery are blacked out. This approach key semantic content. The hypothesis of online is as naive as it seems, but has its own interesting augmentation is that the model probably will not advantages: see the exact same image twice, so memorization

is unlikely, so the model will generalize well.

- It is straightforward to implement.
  - Building the model
- It is fast enough to be used also for online Our model is Convolutional neural network (CNN) learning and preprocess new test data once the composed by 7 levels and one fully collected layer. model has been deployed. Each level is composed by 5 times this structure:
- If original photo is exposed correctly, the blue Convolutional layer, batch normalization and ReLu sky and the greenery are removed optimally. Activation. Between two levels there is a Max- Pooling layer, but in the final one we have an

the downsides are: Average-Pooling layer.

- The absence of morphological analysis pre- 4 Performance evaluation

vent the detection and the extraction of more

complex elements, such as manmade object, 4.1 Comparison with other algorithms

human shapes and so on.

Table 1: Accuracy table

- It may happen that if a building has either many windows or it is a glass building, then the reflection of the sky on it may trick the algorithm causing the erosion of important portion of image, i.e. loss of useful informa- tion.

|- classes|DPM-LSVM|MLLR+SP|Our Solution|
| - | - | - | - |
|10|65.67%|69.17%|-|
|25|37.69%|46.21%|63.43%|
Performances obtained by using the Xu’s original dataset

Our system outperforms all the others when us-

- It may happen that, even if not visible to a ingtheoriginaldatasetandcomparingtheaccuracy. the naked eye, hues of colors to be removed

are present in some area we would like to

preserve. However, taking in consideration the kind of task we are dealing with and the different sizes of

4. K-means Clustering

datasets involved, we believe that the accuracy is To tackle the last downside, applying colors k- a poor choice when estimating the level of perfor-

means clusterization and reducing the color palette mance: computing the accuracy of an imbalanced to the dominant ones, generally improves the cor- problem such this one, the results are obviously rect isolation of the parts we want to save from the skewed. For this reason, we have adopted the more ones that can be discarded (in this case: blacked (graphically) intuitiveConfusion Matrix. Note that out). Several experiments have been conducted for every class, we have added the

to choose the best k value, and the results suggest recognition rate: #correctidentifications to better

#classinstancesintestset

that an interval from 6 to 12 seems to work fine; understand how does the system perform when an- however, notice that the closer we get to the lower alyzing more images per class.

bound, the faster the algorithm will be.

![](Aspose.Words.73d9cb93-52ad-4b0f-95a8-05591ad154ae.001.png)

1) Dumitru’s result on enlarged dataset

![](Aspose.Words.73d9cb93-52ad-4b0f-95a8-05591ad154ae.002.png)![](Aspose.Words.73d9cb93-52ad-4b0f-95a8-05591ad154ae.003.png)

2) Our result on enlarged dataset (c) Our result on enlarged pre-processed dataset Figure 1: Comparing the confusion matrices

5 Final notes

At this stage, from (a), (b) and (c) it is immedi- ately visible that Dumitru’s system does a better job in categorizing each architectural style. How- ever, from (b) and (c), we can see that better re- sults are obtained when the algorithm described in[ Preprocessing ](#_page0_x307.28_y416.24)is applied. As supposed by Du- mitru when experimenting with different version of resnet, to choose of a deeper neural network can heavily influence the outcomes: more layers and parameters probably lead to better results. Further investigation and experimenting could easily take to even higher performances. A first step in this direction would be merging the two approach: pre- pare the data with a refined algorithm and train a deeper network.
