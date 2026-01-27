## 🎯 GOAL Project — Intelligent Container Inspection System
Inspection automation container using Vision + AI reasoning

## ♺ Workflow project:
![alt text](images/3E4D1E97-2611-4CA7-A5D5-EE35CD88749C.png)

## 🔹 Goals project:

### **1️⃣ Image Classification & Damage Detection**

- Detect: dent, rust, broken door, leak
- Classify: normal vs damaged
- Output severity level

### 2️⃣ RAG SOP & Compliance Engine

- Find SOP handling for broken container
- Answering shipment regulation
- Generate action recommendation

### 3️⃣ Risk Management Engine

- Count operational risk score
- Financial loss estimation
- Decision: allow / hold / reject shipment

# 📝 Logs progress

- Create raw table for Joining on staging SQL table
- Create schema sql classification table
- Load container images dataset and display in notebook as iterable
- Create visualize dashboard for Logistic-RAG Equivalent to ensure the classify container which are damaged vs normal
- Merged container image with sixth SQL components dataset
    1. CUMULATIVE INSPECTION METRIC
    2. DAILY PERFORMANCE LINE
    3. MONTHLY HEATMAP (LIKE IMAGE)
    4. YEARLY BAR PERFORMANCE
    5. DISTRIBUTION HISTOGRAM
    6. UANTILE PLOT (MODEL STABILITY)
- CORE IDEA such as engineering vocabulary
    - YOLO + vision = event generator
    - Visualizer on Streamlit = trend analyzer
    - RAG Engine = policy reasoning layer
    - Risk Engine = decision scorer
- Merge dataframe raw + YOLO container manipulation different database raw = Inspection Feature Mart
- Create Inspection Feature Mart with create new SQL logistics.container_registry and export to CSV for next feature inspection
- Data Modeling between YOLO container and dataframe CSV in merged
- Data modeling as result as Inspection Feature Mart is done.
- Continue in workflow Feast feature store for handling in Training dataset (ml engineering concept) to get result with ML Model (Risk/Defect prediction) → Online Inference
- Next in AI Engineering concept with llama3 model to improve dataset by prompting to ensure products relevant to dataset
- Training for RAG embedding experiment using YOLOv8 model in Notebook
- **TensorFlow SavedModel:** export success ✅ 224.6s have trained images using YOLOv8
    
    Training inference results
    
    - Detecting conttainer ID
    
    ![train_batch2.jpg](attachment:afd5e4f8-b5e9-469f-9d0b-bbf899d0fe80:train_batch2.jpg)
    
    - Predicting confidence dent container
    
    ![val_batch1_pred.jpg](attachment:268a8873-7931-4d6c-aa09-66c33d1639d1:val_batch1_pred.jpg)
    
    - Validating confidence dent container
    
    ![val_batch1_labels.jpg](attachment:97bac86a-d230-4a15-971c-f2e1a38962c3:val_batch1_labels.jpg)
    
    - Validation container detection
    
    ![val_batch0_pred.jpg](attachment:71beeb88-4ace-45fe-84ca-2bd44a251b85:val_batch0_pred.jpg)
    
    ![val_batch0_labels.jpg](attachment:a8d56319-055b-4f2a-8538-67f79d653671:val_batch0_labels.jpg)
    
    - Metrics confidence curve container detection
    
    ![BoxF1_curve.png](attachment:a5fb192c-d755-465d-9bb5-f2f2f572fc3b:BoxF1_curve.png)
    
    ![BoxP_curve.png](attachment:cad8d7ec-1092-46a2-869e-8f290a8f7feb:BoxP_curve.png)
    
    ![BoxPR_curve.png](attachment:2e069906-83b5-482f-8627-b87d1ea419c9:BoxPR_curve.png)
    
    ![BoxR_curve.png](attachment:a3a01f90-cfa5-48d2-bacc-50342128a2df:BoxR_curve.png)
    
    ![confusion_matrix_normalized.png](attachment:9405ce6d-ae2d-40ef-850e-de129b8445a7:confusion_matrix_normalized.png)
    
    ![confusion_matrix.png](attachment:6c65e2c2-de44-4796-a60a-ca3bce25e6a4:confusion_matrix.png)
    
![alt text](images/container.png)
    
-