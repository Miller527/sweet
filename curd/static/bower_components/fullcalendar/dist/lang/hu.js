(function(e){"function"==typeof define&&define.amd?define(["../../../jquery/jquery","moment"],e):e(jQuery,moment)})(function(e, t){function n(e, t, n, a){var r=e;switch(n){case"s":return a||t?"néhány másodperc":"néhány másodperce";case"m":return"egy"+(a||t?" perc":" perce");case"mm":return r+(a||t?" perc":" perce");case"h":return"egy"+(a||t?" óra":" órája");case"hh":return r+(a||t?" óra":" órája");case"d":return"egy"+(a||t?" nap":" napja");case"dd":return r+(a||t?" nap":" napja");case"M":return"egy"+(a||t?" hónap":" hónapja");case"MM":return r+(a||t?" hónap":" hónapja");case"y":return"egy"+(a||t?" év":" éve");case"yy":return r+(a||t?" év":" éve")}return""}function a(e){return(e?"":"[múlt] ")+"["+r[this.day()]+"] LT[-kor]"}var r="vasárnap hétfőn kedden szerdán csütörtökön pénteken szombaton".split(" ");t.lang("hu",{months:"január_február_március_április_május_június_július_augusztus_szeptember_október_november_december".split("_"),monthsShort:"jan_feb_márc_ápr_máj_jún_júl_aug_szept_okt_nov_dec".split("_"),weekdays:"vasárnap_hétfő_kedd_szerda_csütörtök_péntek_szombat".split("_"),weekdaysShort:"vas_hét_kedd_sze_csüt_pén_szo".split("_"),weekdaysMin:"v_h_k_sze_cs_p_szo".split("_"),longDateFormat:{LT:"H:mm",L:"YYYY.MM.DD.",LL:"YYYY. MMMM D.",LLL:"YYYY. MMMM D., LT",LLLL:"YYYY. MMMM D., dddd LT"},meridiem:function(e,t,n){return 12>e?n===!0?"de":"DE":n===!0?"du":"DU"},calendar:{sameDay:"[ma] LT[-kor]",nextDay:"[holnap] LT[-kor]",nextWeek:function(){return a.call(this,!0)},lastDay:"[tegnap] LT[-kor]",lastWeek:function(){return a.call(this,!1)},sameElse:"L"},relativeTime:{future:"%s múlva",past:"%s",s:n,m:n,mm:n,h:n,hh:n,d:n,dd:n,M:n,MM:n,y:n,yy:n},ordinal:"%d.",week:{dow:1,doy:7}}),e.fullCalendar.datepickerLang("hu","hu",{closeText:"bezár",prevText:"vissza",nextText:"előre",currentText:"ma",monthNames:["Január","Február","Március","Április","Május","Június","Július","Augusztus","Szeptember","Október","November","December"],monthNamesShort:["Jan","Feb","Már","Ápr","Máj","Jún","Júl","Aug","Szep","Okt","Nov","Dec"],dayNames:["Vasárnap","Hétfő","Kedd","Szerda","Csütörtök","Péntek","Szombat"],dayNamesShort:["Vas","Hét","Ked","Sze","Csü","Pén","Szo"],dayNamesMin:["V","H","K","Sze","Cs","P","Szo"],weekHeader:"Hét",dateFormat:"yy.mm.dd.",firstDay:1,isRTL:!1,showMonthAfterYear:!0,yearSuffix:""}),e.fullCalendar.lang("hu",{defaultButtonText:{month:"Hónap",week:"Hét",day:"Nap",list:"Napló"},allDayText:"Egész nap"})});