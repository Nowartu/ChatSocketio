if(!self.define){let e,s={};const i=(i,n)=>(i=new URL(i+".js",n).href,s[i]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=i,e.onload=s,document.head.appendChild(e)}else e=i,importScripts(i),s()})).then((()=>{let e=s[i];if(!e)throw new Error(`Module ${i} didn’t register its module`);return e})));self.define=(n,r)=>{const t=e||("document"in self?document.currentScript.src:"")||location.href;if(s[t])return;let o={};const c=e=>i(e,t),l={module:{uri:t},exports:o,require:c};s[t]=Promise.all(n.map((e=>l[e]||c(e)))).then((e=>(r(...e),o)))}}define(["./workbox-e3490c72"],(function(e){"use strict";self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"assets/index-BwTI6MsR.js",revision:null},{url:"assets/index-CT6a4P7g.css",revision:null},{url:"index.html",revision:"4b2bd4a1bdcab3e8a1e6e51662284014"},{url:"registerSW.js",revision:"402b66900e731ca748771b6fc5e7a068"},{url:"pwa-192x192.png",revision:"e8f1c5efefd302087e45b217b9d695cf"},{url:"pwa-512x512.png",revision:"9353788efac8a43d827a04b5cd9349db"},{url:"pwa-maskable-192x192.png",revision:"e5fca47d821561805cf1cbc461e13816"},{url:"pwa-maskable-512x512.png",revision:"e5ab4e14ed8c3e7194464459f586acf7"},{url:"manifest.webmanifest",revision:"14f516d91a46821252accba865e5b64b"}],{}),e.cleanupOutdatedCaches(),e.registerRoute(new e.NavigationRoute(e.createHandlerBoundToURL("index.html")))}));
