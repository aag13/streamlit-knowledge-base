# Streamlit Knowledge Base App

This project contains the source code and supporting files for a streamlit application 
that implements a Knowledge Base. The backend application code to support this app can be 
found in this repository, [Opensearch Knowledge base](https://github.com/CloudBazar/opensearch-knowledge-base)

The app contains four pages:

- Dashboard - The landing page for the app.
- Add Document - To create documents for ingestion in *Amazon Opensearch*.
- Search Documents - Search documents using *Category* and *search text*.
- Update Documents - Update an already indexed document in *Opensearch*.

## How to deploy your own app

Follow these steps to deploy the app on Streamlit Community Cloud account,
* Clone this repository on your machine
* create a *secrets.toml* file inside *.streamlit/* directory.
* Add the following code in the *secrets.toml* file.
```toml
[params]
category_list = ["Admin", "App", "Backend", "Business"]
api_base_endpoint = "YOUR_API_ENDPOINT_INCLUDING_INDEX_NAME"
doc_path = "NAME_OF_YOUR_RESOURCE_PATH"
load_bg = true
bg_img_url = "https://images.unsplash.com/photo-1551554781-c46200ea959d"
```
* Explanation of these parameters:
  * **category_list** : List of category for your documents. You can add/remove from
  this list without changing anything in the backend.
  * **api_base_endpoint** : The base URL for the APIs in the backend including the name 
  of the index in your Opensearch. E.g, if the base URL of your APIs is `https://xxxxxxxx.execute-api.narnia-east-101.amazonaws.com/stage` and 
  name of the index created in Opensearch is `wowow`, then the *api_base_endpoint* is set to 
  `https://xxxxxxxx.execute-api.narnia-east-101.amazonaws.com/stage/wowow`
  * **doc_path** : This is the root resource path identifying your documents. If you use the provided 
  backend application then the root resource path will be `kb-docs`. Find the API endpoints 
  that is used by this application based on the configuration above to get a better understanding. 
    * Create document (**POST**): https://xxxxxxxx.execute-api.narnia-east-101.amazonaws.com/stage/wowow/kb-docs
    * Update document (**PUT**): https://xxxxxxxx.execute-api.narnia-east-101.amazonaws.com/stage/wowow/kb-docs/{doc_id}
    * Get document (**GET**): https://xxxxxxxx.execute-api.narnia-east-101.amazonaws.com/stage/wowow/kb-docs/{doc_id}
    * Search documents (**POST**): https://xxxxxxxx.execute-api.narnia-east-101.amazonaws.com/stage/wowow/kb-docs/search
  * **load_bg** : Whether to load a background image. Value: true or false
  * **bg_img_url** : The URL from which to download the background image.

*Update this parameter according to your backend API resource path*.

You can now deploy this app in your own instance through Nginx web server. 

However, if you want to deploy the app on Streamlit Community Cloud, make sure to put 
the `secrets.toml` file in `.gitignore` file to make git not track it to prevent it from being 
pushed in GitHub. Then during the deployment of the app on Streamlit Community Cloud, add the content of 
the `secrets.toml` file in the `Advanced Setting` section.
