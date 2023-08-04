# Model card for recsys23

Last updated: <Month> <Year>

Inspired by [Model Cards for Model Reporting (Mitchell et al.)](https://arxiv.org/abs/1810.03993), we’re providing some 
accompanying information about the XXXXX models we're releasing.

## Model description

This model was developed by researchers at **Fraunhofer AICOS** to help us understand how the capabilities of ...

### Model date

<Month> <Year>, trained on data that cuts off at the end of <Year>.

### Model type



### Model version

XXXX parameters. We have also released XXXX million parameter models.

### Paper or other resource for more information

[Blog post]() and [paper]()

### Where to send questions or comments about the model

Please use this

## Intended Uses:

### Primary intended uses

The primary intended users of these models are *AI researchers and practitioners*.

We primarily imagine these models will be used by researchers to better understand the behaviors, capabilities, 
biases, and constraints of ...

### Secondary uses

Here are some secondary use cases we believe are likely:

- 
- 
- 

### Out-of-scope use cases

Additionally, models like XXXX reflect the biases inherent to the systems they were trained on, so we do not recommend 
that they be deployed into systems that interact with humans unless the deployers first carry out a study of biases 
relevant to the intended use-case. We found no statistically significant difference in gender, race, and religious bias 
probes all versions of XXXX should be approached with similar levels of caution around use cases that are sensitive to 
biases around human attributes.

## Evaluation Data

### Datasets

This model was trained on (and evaluated against) YYYY dataset, a dataset consisting of the (...).

To get a sense of the data that went into XXXXX, we’ve (...).

## Ethical Considerations



### Caveats and Recommendations

Because XXXXX model, it’s currently difficult to know what disciplined testing procedures can be applied to it to fully
understand its capabilities and how the data it is trained on influences its vast range of outputs. We recommend researchers
investigate these aspects of the model and share their results.

Additionally, as indicated in our discussion of issues relating to potential misuse of the model, it remains unclear what
the long-term dynamics are of detecting outputs from these models. We conducted some experiments using simple classifiers, 
(...), and fine-tuning methods.

Our fine-tuned detector model reached accuracy levels of approximately ZZ%. However, no one detection method is a panacea;
automated ML-based detection, human detection, human-machine teaming, and metadata-based detection are all methods that 
can be combined for more confident classification. Developing better approaches to detection today will give us greater 
intuitions when thinking about future models and could help us understand ahead of time if detection methods will 
eventually become ineffective.
