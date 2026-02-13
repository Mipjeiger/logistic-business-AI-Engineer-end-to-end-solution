## 🎯 GOAL Project — Intelligent Container Inspection System
Inspection automation container using Vision + AI reasoning

## ♺ Workflow project:
![alt text](images/workflow-engineer.png)

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
![alt text](images/container.png)
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
    
    ![alt text](images/train_batch2.jpg)
    
    - Predicting confidence dent container
    
    ![val_batch1_pred.jpg](images/val_batch1_pred.jpg)
    
    - Validating confidence dent container
    
    ![val_batch1_labels.jpg](images/val_batch1_labels.jpg)
    
    - Validation container detection
    
    ![val_batch0_pred.jpg](images/val_batch0_pred.jpg)
    
    ![val_batch0_labels.jpg](images/val_batch0_labels.jpg)
    
    - Metrics confidence curve container detection
    
    ![BoxF1_curve.png](images/BoxF1_curve.png)
    
    ![BoxP_curve.png](images/BoxP_curve.png)
    
    ![BoxPR_curve.png](images/BoxPR_curve.png)
    
    ![BoxR_curve.png](images/BoxR_curve.png)
    
    ![confusion_matrix_normalized.png](images/confusion_matrix_normalized.png)
    
    ![confusion_matrix.png](images/confusion_matrix.png)

- Ingesting container video from youtube for training in RAG experiment using YOLOV8 model dataset are trained before
- Real-time container detection using YOLOV8 model. These are result of detection
    
    ![2E2BB404-FD73-48AB-BBA5-84FDF2276EBD.png](attachment:d3dca40d-9451-4485-9be4-f20ffe074618:a97c7df5-9c23-4f5a-aa79-dc89cdaac21e.png)
    
- Create VectorDB for AI Engineer concept RAG Experiment layer
    
    ![Screenshot 2026-01-27 at 22.55.35.png](attachment:6f6602ec-0b1d-4002-87f0-c8b31fca08fd:Screenshot_2026-01-27_at_22.55.35.png)
    
- LLama3 models is fething with SOP docs
    
    ![EF492538-57A0-42FC-B02C-446C3D58F225.png](attachment:f907bef6-5c49-410d-8999-903a48ca9b2d:EF492538-57A0-42FC-B02C-446C3D58F225.png)
    
- Result generating AI prompt engineering for business recommendations
- Use PDF document for integrating FAISS in comprehensive interpretability prompt
    
    ![D0511F27-2655-4CE5-A5B0-9A79EC25293E.png](attachment:b25cb572-0680-4e94-8e47-729a8c0c0224:D0511F27-2655-4CE5-A5B0-9A79EC25293E.png)
    
- Create THRESHOLD in notebook with model for calibration data train to ensure the threshold is relevant to SQL dataset
- Debugging in-relevant thresholds because dissyncronize with big gap data between df.describe() (statistics method) Note: Debug THRESHOLDS first before go for slack notifier
- Set slack environment for slack notification in production based on severity score inspection qualified. export SLACK_WEBHOOK_URL first to ensure echo $SLACK_WEBHOOK_URL is reliable to project
- Slack production for inspecting image result based http://localhost:8000/inspect-image on API endpoint in postman with variable:
    
    shipment_id: str,
    severity_score: float,
    alert_level: str,
    class_name: str
    
    Results:
    
    ![Screenshot 2026-01-30 at 15.07.55.png](attachment:bcfe84f6-ba20-407d-8e1b-fde432863047:Screenshot_2026-01-30_at_15.07.55.png)
    
    ![Screenshot 2026-01-30 at 15.19.18.png](attachment:d6452738-efdd-49c2-8d5b-d3a9fc541dc7:Screenshot_2026-01-30_at_15.19.18.png)
    
- Postman as API endpoint test [localhost/inspect-image](http://localhost/inspect-image) result on postman
    
    ![8AB64A0F-D69A-4606-8EC9-72D608D1ACFE.png](attachment:d08639b5-6be8-4123-ad00-262788c269c1:8AB64A0F-D69A-4606-8EC9-72D608D1ACFE.png)
    
- Deploying machine learning model on logistic-rag project + deploying finetuning LLM & RAG AI Engineering on ❄️Snowflake deployment
- Create DATABASE, WAREHOUSE, SCHEMA, STAGE in snowflake environment. Snowflake databases are different with PostgreSQL database
    
    ![2A06F7F6-E755-4342-A96B-54F80AD49488.png](attachment:e1cb5fc2-eda1-445c-afe5-0e2d64b0b16e:2A06F7F6-E755-4342-A96B-54F80AD49488.png)
    
- Wrapped API in docker images and container as containerization for API model wrapper deployment
    
    ![Screenshot 2026-01-31 at 16.05.56.png](attachment:2cb0cd4a-55d5-473a-a314-487b10d32657:Screenshot_2026-01-31_at_16.05.56.png)
    
- Build machine learning models and resulting feature importance for dataset prediction

![image.png](attachment:c2b86516-4616-4ea2-8a84-0dbe85b12c4c:image.png)

![image.png](attachment:5ce20829-8ee5-48d0-ba31-4a827559b2f8:image.png)

![image.png](attachment:a118fb40-1608-43f5-9c5c-08d6b353a05a:image.png)

![image.png](attachment:ae06e11f-382a-4469-b7c9-02038ece2005:image.png)

![image.png](attachment:12268151-792f-4d7a-992a-53eb36a5c6bc:image.png)

- Deployed YOLOV8 model on container inspection logistic-rag for images and videos detection
    
    Container images inspection:
    
    ![26ADEA67-0C64-4AD3-81A4-79D1AA39393E.png](attachment:4a6a466e-b091-4a56-b079-73c7c5376993:26ADEA67-0C64-4AD3-81A4-79D1AA39393E.png)
    
    ![43DBBC7F-98FE-42E9-89AB-E5F74CFCBD47.png](attachment:c5d01840-986a-4907-8517-bb2ad800f73f:43DBBC7F-98FE-42E9-89AB-E5F74CFCBD47.png)
    
    Container videos inspection:
    
- Training model container dataset for damage container inspection using computer vision using YOLOV8 model
    
    ![4C1271C7-E562-4427-980C-ED8393A38BD3.png](attachment:39b1b31e-0b62-450f-b666-b9dd58148470:4C1271C7-E562-4427-980C-ED8393A38BD3.png)
    
- Training model container dataset for container classification detection
    
    ![A277A5D4-3068-45B1-817E-420CDEC36E34.png](attachment:01d83031-9fc2-4ffe-86ec-b18551a739a6:A277A5D4-3068-45B1-817E-420CDEC36E34.png)
    
- Epochs training using 100 epoch with patience=15 and stopped in 39/100 epocs training no models improvement
    
    ![2.png](attachment:1bea1bd8-2b39-4a77-875b-44c47ae3ee46:62d29816-d57e-4de5-8c5d-e4ea276ce828.png)
    
- Epochs training using 100 epoch with patience=10 and stopped in 35/100 epocs training because no models improvement
    
    ![565886EE-7AA2-42B2-80FC-ABCBD16C0029.png](attachment:2a78fc2b-dc9b-4850-aea2-c7340cb54a7c:565886EE-7AA2-42B2-80FC-ABCBD16C0029.png)
    
- Validation and visualization test with image and retrieve array result from images trained
    
    ![60EC1A4B-C96D-4EB8-8A61-29A2FC128257.png](attachment:b1e94c20-5505-4c53-b21b-75c4c664244f:60EC1A4B-C96D-4EB8-8A61-29A2FC128257.png)
    
- Validation test with image and retrieve array result from images trained
    
    ![1.png](attachment:83232e63-b72a-4556-a871-89bff56f552a:1.png)
    
- Best metrics result from [best.pt](http://best.pt) YOLOV8 model was trained for improving model
    
    ![output-rag.png](attachment:4ac90950-00ac-4b09-a2a1-2e9457a8628d:output-rag.png)
    
    ![output-validation rag metrics.png](attachment:0735f3a7-71e2-4eb0-bf91-c1cacb8fbe8a:output-validation_rag_metrics.png)
    
- Video inspection container damage result with CLASS_MAP for identyfing DAMAGE and Container classification. ROI_DEBUG added for better performance to prevent false positive values
    
    ![alt text](images/img25.png)
    
    ![alt text](images/img26.png)
    
- Still caught up on container vision even the drone getting higher
    
    ![alt text](images/img27.png)
    
- Videos
    
    ![alt text](images/output_mb.gif)
    
- Creating RAG Experimennt Layer and Create Vector DB embbeding use HuggingFace on (sentence-transformers/all-MiniLM-L6-v2) model name for read documents
- Finetuning LLM with OllamaLLM using llama3 model
    
    ![alt text](images/img28.png)
    
- Prompting AI Engineering result using OllamaLLM
    
    ![alt text](images/img29.png)
    
- Prompting full AI Generative results
    - 🤖 Generating AI business recommendation...
    
    ```
        ╔══════════════════════════════════════════════════════════════╗
        ║                 AI BUSINESS RECOMMENDATION                  ║
        ╠══════════════════════════════════════════════════════════════╣
        ║  **Risk Category:** Based on the inspection data and SOP    ║
        ║  context, I categorize the risk as **MEDIUM**. The severity ║
        ║  score of 4 indicates a moderate level of risk due to the   ║
        ║  presence of rust (2 containers) which could lead to        ║
        ║  structural damage or contamination of cargo.               ║
        ║                                                              ║
        ║  **Immediate Operational Action:** Recommend that all       ║
        ║  containers with rust damage be removed from service        ║
        ║  immediately and sent for repair to prevent any potential   ║
        ║  hazards.                                                   ║
        ║                                                              ║
        ║  **Repair Urgency:** The urgency of repair is **MEDIUM**.   ║
        ║  While it is essential to address the rust damage promptly, ║
        ║  it is not a critical issue requiring immediate attention.  ║
        ║  A timeline for repair should be established, taking into   ║
        ║  account the container's current usage and planned          ║
        ║  maintenance schedule.                                      ║
        ║                                                              ║
        ║  **Safety Mitigation:**                                     ║
        ║                                                              ║
        ║  1. Implement additional inspections on containers with     ║
        ║  rust damage to ensure the severity of the damage is        ║
        ║  accurately assessed.                                       ║
        ║  2. Conduct regular inspections of all containers to        ║
        ║  prevent similar issues from arising in the future.         ║
        ║  3. Develop a plan to address any underlying causes         ║
        ║  contributing to the rust damage, such as inadequate        ║
        ║  cleaning or poor storage conditions.                       ║
        ║                                                              ║
        ║  **Executive Summary:**                                     ║
        ║  The drone inspection result reveals 20 containers with no  ║
        ║  significant structural damage, but two containers          ║
        ║  exhibiting rust damage. This presents a moderate risk      ║
        ║  level, requiring prompt attention to prevent potential     ║
        ║  hazards. I recommend removing these containers from        ║
        ║  service and sending them for repair. A medium-level        ║
        ║  urgency is assigned for repair, considering the            ║
        ║  container's current usage and planned maintenance          ║
        ║  schedule. To mitigate this risk, additional inspections    ║
        ║  should be conducted, and a plan developed to address any   ║
        ║  underlying causes contributing to the rust damage.         ║
        ║                                                              ║
        ║  **Detailed Explanation:**                                  ║
        ║  The drone inspection result provides valuable insights     ║
        ║  into the condition of the containers. The absence of       ║
        ║  dents, broken doors, or leaks indicates that the           ║
        ║  containers are generally in good condition. However, the   ║
        ║  presence of rust damage in two containers poses a moderate ║
        ║  risk level. Rust can compromise the structural integrity   ║
        ║  of the container and contaminate cargo, making it          ║
        ║  essential to address this issue promptly.                  ║
        ║                                                              ║
        ║  The severity score of 4, based on the inspection data,     ║
        ║  supports the categorization of the risk as MEDIUM. This    ║
        ║  rating takes into account the potential consequences of    ║
        ║  inaction, including damage to the container or             ║
        ║  contamination of cargo, which could result in significant  ║
        ║  economic losses or even compromise food safety.            ║
        ║                                                              ║
        ║  To mitigate this risk, I recommend removing the containers ║
        ║  with rust damage from service and sending them for repair. ║
        ║  A medium-level urgency is assigned for repair, considering ║
        ║  the container's current usage and planned maintenance      ║
        ║  schedule. This allows for a reasonable timeframe to        ║
        ║  complete the repairs while still ensuring prompt attention ║
        ║  is given to prevent potential hazards.                     ║
        ║                                                              ║
        ║  In addition to addressing the rust damage, it is essential ║
        ║  to implement additional inspections on containers with     ║
        ║  similar issues to ensure the severity of the damage is     ║
        ║  accurately assessed. Regular inspections of all containers ║
        ║  should also be conducted to prevent similar issues from    ║
        ║  arising in the future. A plan should be developed to       ║
        ║  address any underlying causes contributing to the rust     ║
        ║  damage, such as inadequate cleaning or poor storage        ║
        ║  conditions.                                                ║
        ║                                                              ║
        ║  By taking these steps, we can minimize the risk associated ║
        ║  with rusty containers and ensure the safe transportation   ║
        ║  of goods while maintaining compliance with relevant        ║
        ║  regulations and standards.                                 ║
        ╚══════════════════════════════════════════════════════════════╝
    
    ```
    
    # ================================================================================
    RAW OUTPUT (for logging):
    
    **Risk Category:** Based on the inspection data and SOP context, I categorize the risk as **MEDIUM**. The severity score of 4 indicates a moderate level of risk due to the presence of rust (2 containers) which could lead to structural damage or contamination of cargo.
    
    **Immediate Operational Action:** Recommend that all containers with rust damage be removed from service immediately and sent for repair to prevent any potential hazards.
    
    **Repair Urgency:** The urgency of repair is **MEDIUM**. While it is essential to address the rust damage promptly, it is not a critical issue requiring immediate attention. A timeline for repair should be established, taking into account the container's current usage and planned maintenance schedule.
    
    **Safety Mitigation:**
    
    1. Implement additional inspections on containers with rust damage to ensure the severity of the damage is accurately assessed.
    2. Conduct regular inspections of all containers to prevent similar issues from arising in the future.
    3. Develop a plan to address any underlying causes contributing to the rust damage, such as inadequate cleaning or poor storage conditions.
    
    **Executive Summary:**
    The drone inspection result reveals 20 containers with no significant structural damage, but two containers exhibiting rust damage. This presents a moderate risk level, requiring prompt attention to prevent potential hazards. I recommend removing these containers from service and sending them for repair. A medium-level urgency is assigned for repair, considering the container's current usage and planned maintenance schedule. To mitigate this risk, additional inspections should be conducted, and a plan developed to address any underlying causes contributing to the rust damage.
    
    **Detailed Explanation:**
    The drone inspection result provides valuable insights into the condition of the containers. The absence of dents, broken doors, or leaks indicates that the containers are generally in good condition. However, the presence of rust damage in two containers poses a moderate risk level. Rust can compromise the structural integrity of the container and contaminate cargo, making it essential to address this issue promptly.
    
    The severity score of 4, based on the inspection data, supports the categorization of the risk as MEDIUM. This rating takes into account the potential consequences of inaction, including damage to the container or contamination of cargo, which could result in significant economic losses or even compromise food safety.
    
    To mitigate this risk, I recommend removing the containers with rust damage from service and sending them for repair. A medium-level urgency is assigned for repair, considering the container's current usage and planned maintenance schedule. This allows for a reasonable timeframe to complete the repairs while still ensuring prompt attention is given to prevent potential hazards.
    
    In addition to addressing the rust damage, it is essential to implement additional inspections on containers with similar issues to ensure the severity of the damage is accurately assessed. Regular inspections of all containers should also be conducted to prevent similar issues from arising in the future. A plan should be developed to address any underlying causes contributing to the rust damage, such as inadequate cleaning or poor storage conditions.
    
    # By taking these steps, we can minimize the risk associated with rusty containers and ensure the safe transportation of goods while maintaining compliance with relevant regulations and standards.
    

# Next step on MLOps system inference 🤖

- Docker contenarize components because Model is fetched **at container startup**.
    - Python runtime
    - FastAPI app
    - MLflow client
    - Inference logic
- Docker contenarize mlflow + minio + minio-init are bing wrapped in Dockerfile
    
    ![alt text](images/img30.png)
    
- Remove minio-init because of MinIO will work without pre-created buckets
    
    ![alt text](images/img31.png)
    
- MLflow Tracking & Registry models
    
    ![alt text](images/img32.png)
    
    ![alt text](images/img33.png)
    
- MLflow metrics result
    
    ![alt text](images/img34.png)
    
- Machine learning models in minio storage
    
    ![alt text](images/img35.png)
    
- YOLOV8 model in minio storage
    
    ![alt text](images/img36.png)
    
- RAG model in minio storage
    
    ![alt text](images/img37.png)
    
- Push to Dockerhub
    
    ![alt text](images/img38.png)
    
- Build docker-compose.yml for inference system with adding Grafana, Prometheus, Streamlit, API, Minio, MLFlow.
    
    ![alt text](images/img39.png)
    
- Slack receiving notifications which are triggered by API calls
- (result)
- Deploy result model to streamlit (UI 💻) as interface for user
- (result)
- Prometheus model metrics and Grafana visualization to display model metrics inference
- (result)
- Kubernetes for latency deployment inference serving
- (result)
- CI/CD Pipelines automation inference integrating
- (result)
- Deploy model to railway cloud (Railway deployment 💼)
- (result)
- 
- Build dockerfile images with purpose to push on dockerhub. After has been pushed, pull multimodel-api from dockerhub for retrieving coherent in deployment
    
    ![alt text](images/img40.png)
    
- MLOps FastAPI [localhost](http://localhost) components
    
    ![alt text](images/img41.png)
    
- Deployment services API in railway
    
    ![alt text](images/img42.png)
    
    - API deployment in railway hosting cloud
        
        ![alt text](images/img43.png)
        
    - Inference public API Service by railway deployment
    
    ![alt text](images/img44.png)
    
- Integrated SQL database into  Feature Store and Spark hadoop as Data Features for ingesting in API.
    - Firstly, build EDA (Explore Data Analysis) in notebook for comprehensive machine learning models
    - Data will retrieve good pipelines from notebook’s ready for ingested to Spark hadoop
    - Ingested data on Spark hadoop for making reliable data to send on feature store
- **Decision Intelligence Pipeline source of SQL Database on notebook**:
    - **📸 CV detections (low-level evidence)**
        - **Aggregated inspection features (business-level signals)**
        - **Logistic model (risk scoring)**
        - Supervise learning for classification where container are damaged
        - **RAG (explainability, reasoning, auditability) (Optional)**
- Build container-risk-inspection for comprehensive prediction. Json output expect
    
    ```json
    {	
    "Image": "121_20220503T061259983Z_s00.mp4___1450.jpg"
    
    "model": Logistic Regression
    "predict"" float(result_predict) = example (result for safety shipment depends on predicting is_high_risk is 0.87
    
    "detection_yolo": "this container shipment is 0.9 confidence damaged" or "this container shipment is 0.3 confidence isn't damaged"
    
    "RAG fine tuning LLM": 
    - based on result "this container shipment is 0.9 confidence damaged" is "this container can't carry on shipping because the container is damaged" (note: make a profesional hypothesis based on result)
    - based on result "this container shipment is 0.3 confidence isn't damaged" is "this container can carry on shipping safely (note: make a profesional hypothesis based on result)
    }
    ```
    
- Results of image prediction uploaded
    
    ![alt text](images/img45.png)
    
    ![alt text](images/img46.png)
    
- Deploy and inference to production (PENDING ⌛️)