#!/bin/sh

asar extract app.asar ./app

sed -i 's/jt.a.createElement(hze,{goToSftp:r})/true/g' app/js/ui-process.js