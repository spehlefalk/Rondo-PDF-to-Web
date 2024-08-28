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
let e;chrome.runtime.onMessage.addListener((async function(n){if("offscreen"!==n.target)return!1;if("getUserSubscriptions"!==n.main_op)return console.warn(`Unexpected message type received: '${n.main_op}'.`),!1;!function(n){if(!(window.document.getElementsByTagName("iframe")??[]).length&&n.cdnURL){const t=window.document;e=`${n.cdnURL}#/susi/fetchUserSubscription`;const i=t.createElement("iframe");i.setAttribute("src",e);t.getElementById("cdn-dnr-iframe").appendChild(i)}}(n)})),window.addEventListener("message",(function(n){if(n.origin!==new URL(e).origin)return;const t=n.data;"lastUserGuid"===t.type&&(t.main_op="updateSignInStatus",delete t.type);switch(t?.main_op){case"userSubscriptions":case"updateSignInStatus":chrome.runtime.sendMessage({...t,target:"background",tab:{id:""}})}}));