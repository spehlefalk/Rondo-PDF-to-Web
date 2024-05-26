/*************************************************************************
* ADOBE CONFIDENTIAL
* ___________________
*
*  Copyright 2015 Adobe Systems Incorporated
*  All Rights Reserved.
*
* NOTICE:  All information contained herein is, and remains
* the property of Adobe Systems Incorporated and its suppliers,
* if any.  The intellectual and technical concepts contained
* herein are proprietary to Adobe Systems Incorporated and its
* suppliers and are protected by all applicable intellectual property laws,
* including trade secret and or copyright laws.
* Dissemination of this information or reproduction of this material
* is strictly forbidden unless prior written permission is obtained
* from Adobe Systems Incorporated.
**************************************************************************/
import{analytics as e}from"../common/analytics.js";import{communicate as t}from"./communicate.js";import{util as n}from"./util.js";import{SETTINGS as r}from"./settings.js";import{dcLocalStorage as o}from"../common/local-storage.js";import{downloadManager as s}from"./download-manager.js";import{privateApi as i}from"./private-api.js";import{viewerModuleUtils as a}from"./viewer-module-utils.js";import{floodgate as c}from"./floodgate.js";import{openLocalFteWindow as u}from"./ch-context-menu.js";let l=null,m=chrome.runtime.getURL("viewer.html"),p=!1,f={};chrome.extension.isAllowedFileSchemeAccess((e=>{p=e}));const d=e=>{chrome.tabs.get(e.tabId,(e=>{chrome.runtime.lastError||E(e)}))};function E(e){if(!r.IS_READER&&0!=t.version&&(1!=t.version||0!=t.NMHConnStatus)&&e.url){const t=new URL(e.url);chrome.runtime.id===t.host?(chrome.contextMenus.update("convertPageContextMenu",{visible:!1}),chrome.contextMenus.update("appendPageContextMenu",{visible:!1})):(chrome.contextMenus.update("convertPageContextMenu",{visible:!0}),chrome.contextMenus.update("appendPageContextMenu",{visible:!0}))}}function _(e){const t=new Date;t.setMinutes(t.getMinutes()+r.VIEWER_RECHECK_CDN_ACCESS_DELAY_MINS),o.setItem("netAccAdT",t.getTime()),o.setItem("netAcc",e)}function h(){try{return"true"===o.getItem("pdfViewer")}catch(e){return!1}}function g(e,t){for(let n=0;n<e.length;++n){let r=e[n];if(r.name.toLowerCase()===t)return r}}function I(t){if(void 0!==t.responseHeaders){const n=g(t.responseHeaders,"content-type"),r=g(t.responseHeaders,"content-disposition");if(n){const o=n.value.toLowerCase().split(";",1)[0].trim();if(r&&/^\s*attachment[;]?/i.test(r.value))return!1;if("application/pdf"===o)return!0;if("application/octet-stream"===o){if(r&&/\.pdf(["']|$)/i.test(r.value))return e.event(e.e.VIEWER_PDF_PROCESS_OS_CD),!0;t.url.toLowerCase().indexOf(".pdf")>0&&e.event(e.e.VIEWER_PDF_PROCESS_OS_URL)}}}else if("file"==function(e){let t=e.indexOf("/");return e.substr(0,t-1)}(t.url)&&"PDF"==function(e){if(e)try{let t=new URL(e).pathname;return t.substr(t.lastIndexOf(".")+1).toUpperCase()}catch(e){return""}return""}(t.url))return!0;return!1}const v=async(r,o,i)=>{const a=i.incognito;if("complete"===i.status&&E(i),"loading"===o.status){t.loading({id:r});try{!n.isViewerURL(i.url)||h()&&!a||R(r,function(e,t){t||(t=window.location.href);try{const n=new URL(t);return new URLSearchParams(n.search).get(e)}catch(e){return}}("pdfurl",i.url))}catch(e){}}else if("complete"===o.status){s.newTab(i.url,r);const t=await chrome.extension.isAllowedFileSchemeAccess();i.url.toLowerCase().startsWith("file://")&&i.url.toLowerCase().endsWith(".pdf")&&!t&&(u(i),e.event(e.e.LOCAL_FILE_OPENED))}};function R(e,t){e&&t&&chrome.tabs.update(e,{url:t})}function L(e){if("GET"!==e.method||!r.VIEWER_ENABLED||!h())return!1;let t=e.url,n=`reloadurl-${e.tabId}`;const s=o.getItem(n);if(s&&s===t){try{o.removeItem(n)}catch(e){}return!1}if(!(e=>{if(!e||null===e||"undefined"===e)return!1;let t=[/^chrome\:\/\//,/^chrome\-extension\:\/\//,/^https:\/\/([a-zA-Z\d-]+\.){0,}officeapps.live.com/,/^https\:\/\/*.*\/(saml|login)/,/^https:\/\/sharedcloud.([a-zA-Z\d-]+)+.(s3|s3-accelerate).amazonaws.com/,/^https\:\/\/*.*.\/(login|auth|okta|saml).*\/S*|\/(login|auth|okta|saml|IWA|owa)\//,/^https\:\/\/www.google.com\/search\?q/,/^https\:\/\/www.citibank.*/,/^https:\/\/[^/]*\.*\/([$-/:-?{-~!"^_`\[\]A-Za-z0-9]*)view-sdk/],n=c.getFeatureMeta("dc-cv-invalid-urls");if(n){n=JSON.parse(n);for(let e in n)n[e]=new RegExp(n[e]);t=n}return!![/^http\:\/\/[^/]/,/^https\:\/\/[^/]/,/^file?:/].find((t=>t.test(e)))&&!t.find((t=>t.test(e)))})(t))return!1;const i=I(e);return i}function w(e){try{const t=new URL(e.url),n=new URLSearchParams(t.search);let r=!1;const o=e.initiator;return o&&["https://classroom.google.com","https://mail.google.com","https://drive.google.com"].includes(o)&&n.forEach(((e,t)=>{t.startsWith("print")&&"true"===e&&(r=!0)})),r}catch(e){return!1}}async function C(t){try{if(o.getItem("retryOnNextPage")){await chrome.scripting.executeScript({target:{tabId:t},files:["content_scripts/injectCopyLSIframe.js"]}),await n.sleep(300),e.event(e.e.LOCAL_STORAGE_MIGRATION_RETRYING);const r=await chrome.runtime.sendMessage({main_op:"copy-ls"});chrome.tabs.sendMessage(t,{content_op:"remove-lsCopy"}).catch((()=>null)),"succeed"===r&&(e.event(e.e.LOCAL_STORAGE_MIGRATION_RETRYING_SUCCESS),o.removeItem("retryOnNextPage"),Object.assign(o.storage,await chrome.storage.local.get()))}}catch(e){}}const D=chrome.runtime.getURL("")?.replace(/\/+$/,"");function A(t){t.initiator!==D&&"main_frame"!==t.type&&function(t){if(void 0!==t.responseHeaders){const n=g(t.responseHeaders,"content-type"),r=g(t.responseHeaders,"content-disposition");if(n){const o=n.value.toLowerCase().split(";",1)[0].trim();if("application/pdf"===o)return e.event(e.e.VIEWER_PDF_DETECT_EMBED_PDF_TYPE_PDF),!0;if("application/octet-stream"===o){if(r&&/\.pdf(["']|$)/i.test(r.value))return e.event(e.e.VIEWER_PDF_DETECT_EMBED_PDF_OCTET_CD),!0;if(new URL(t.url).pathname.toLowerCase().endsWith(".pdf"))return e.event(e.e.VIEWER_PDF_DETECT_EMBED_PDF_OCTET_URL),!0}}}return!1}(t)&&e.event(e.e.VIEWER_PDF_DETECT_EMBED_PDF)}function b(t){i.isMimeHandlerAvailable().then((async s=>{const{tabId:i}=t;if(await C(i),o.getItem("sessionStarted")||(o.setItem("sessionId",n.uuid()),o.setItem("sessionStarted",!0)),!s){let o=n.parseExtensionURL(t.url);if(o){o=m+"?pdfurl="+o;let n=t.url.indexOf("#");n>0&&(o+=t.url.slice(n)),r.VIEWER_ENABLED&&h()&&e.event(e.e.VIEWER_EXTN_PDF_OPENED,{tabURL:o}),chrome.tabs.update(i,{url:o})}}}))}function P(r,s){i.isMimeHandlerAvailable().then((async i=>{if(o.getItem("sessionStarted")||(o.setItem("sessionId",n.uuid()),o.setItem("sessionStarted",!0)),i){const e=w(r),t=r.tabId;t>-1&&(f[t]={isGooglePrint:e})}else{if("main_frame"===r.type){const{tabId:n}=r;if(await C(n),!function(){if(!navigator.onLine&&o.getItem("offlineSupportDisable"))return!1;const e=new Date,t=o.getItem("netAcc"),n=o.getItem("netAccAdT");return!(n&&n>e.getTime())||t}()||!L(r))return;if(s&&!p)return void e.event(e.e.VIEWER_PDF_LOCAL_FILE_IGNORED);l=r.url,s&&e.event(e.e.VIEWER_PDF_LOCAL_FILE),a.updateVariables(t.version),a.fetchAndUpdateVersionConfig();let i=function(e){let t=m;if(t+="?pdfurl="+encodeURIComponent(e.url),void 0!==e.responseHeaders){const n=g(e.responseHeaders,"content-length");n&&(t+="&clen="+n.value);const r=g(e.responseHeaders,"accept-ranges");r&&r.value&&"bytes"===r.value.toLowerCase()&&(t+="&chunk=true");const o=g(e.responseHeaders,"content-disposition");if(o&&o.value&&/\.pdf(["']|$)/i.test(o.value)){const e=/filename[^;=\n\*]?=((['"]).*?\2|[^;\n]*)/.exec(o.value);null!=e&&e.length>1&&(t+="&pdffilename="+e[1].replace(/['"]/g,""))}}return w(e)&&(t+="&googlePrint=true"),t}(r);e.event(e.e.VIEWER_EXTN_PDF_OPENED,{tabURL:l});for(let e=0;e<20;e++)try{await chrome.tabs.update(n,{url:i})}catch(e){}}"sub_frame"===r.type&&function(e){return/^https:\/\/[^/]*(acrobat|adobe)\.com\/proxy\/chrome-viewer/.test(e)}(r.url)&&(200!==r.statusCode?403===r.statusCode?(o.setItem("pdfViewer","false"),e.event(e.e.VIEWER_FALLBACK_TO_NATIVE_CDN_FORBIDDEN,{tabURL:r.url}),R(r.tabId,l)):(_(!1),e.event(e.e.VIEWER_FALLBACK_TO_NATIVE_CDN_OFFLINE,{tabURL:r.url}),R(r.tabId,l)):_(!0))}}))}t.registerHandlers({"check-is-google-print":function(e,t,n){return f&&f[e.tabId]?n({isGooglePrint:f[e.tabId].isGooglePrint}):n({isGooglePrint:!1})}});export{P as processRequest,b as honorRequest,d as onTabActivated,v as onTabsUpdated,A as detectEmbeddedPDF};