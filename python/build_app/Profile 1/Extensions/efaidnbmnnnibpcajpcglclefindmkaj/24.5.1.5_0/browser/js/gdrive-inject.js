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
try{const t=Object.keys(window.__initData[0]).filter((t=>"Ca"===t||"Ba"===t))[0];let e=window.__initData[0][t][9][t][35][t][1];document.dispatchEvent(new CustomEvent("userId",{detail:{userId:e}}))}catch(t){document.dispatchEvent(new CustomEvent("userId",{detail:{userId:""}}))}