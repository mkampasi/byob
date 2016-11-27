$(function(){

   console.log("setSillsProfile.js loaded!");

   //plug json array objects here 

   var allLanguages = jQuery.parseJSON('{"languages" : ["Java","CPP","C","Python"]}');
   var selectedLanguages = jQuery.parseJSON('{"languages" : ["Ruby","Scala"]}');

   var allfos = jQuery.parseJSON('{"fos" : ["Machine Learning","Artificial Intelligence","Game Development","Android"]}');
   var selectedfos = jQuery.parseJSON('{"fos" : ["IOS","Ruby on Rails"]}');

   
   POPULATE_LISTS = {
   	populate: function(className, jsonArray){
   		console.log("Class name is ::" + className);

   		$.each(jsonArray,function(i,lang){
		   	
		   	var listItem = "";
		   	if(className == "languageSelectedList" || className == "fosSelectedList")
		   		listItem = "<li class='ui-state-highlight'>"+ lang +"</li>"
		   	else
		   		listItem = "<li class='ui-state-default'>"+ lang +"</li>"

		   	$(listItem).appendTo("."+className);
		   	
		   	// console.log(listItem);
		});
   	}
   }// end of function POPULATE_LISTS


   POPULATE_LISTS.populate("languageList",allLanguages.languages);
   POPULATE_LISTS.populate("languageSelectedList",selectedLanguages.languages);
   POPULATE_LISTS.populate("fosList",allfos.fos);
   POPULATE_LISTS.populate("fosSelectedList",selectedfos.fos);

   
   BUILD_SELECTED_LIST = {
   	build: function(){
   		var sel_lang_arr = new Array();
   		var sel_fos_arr = new Array();
   		var selectedJsonOBJ = {};

   		$(".languageSelectedList li").each(function(){
   			sel_lang_arr.push($(this).text());
   		});

   		selectedJsonOBJ["selectedLang"] = sel_lang_arr;

   		$(".fosSelectedList li").each(function(){
   			sel_fos_arr.push($(this).text());
   		});

   		selectedJsonOBJ["selectedFOS"] = sel_fos_arr;

   		return selectedJsonOBJ;

   	} 
   }//end of BUILD_SELECTED_LIST

   $("#getStarted").click(function(){
      var userJSONObj = BUILD_SELECTED_LIST.build();  // This is final user selected languages and FOS object      
      console.log(userJSONObj);
      alert("Skills saved!");
   });





});