
// [7:15 PM, 11/28/2016] Manisha USC: it was export FLASK_APP=flask_app.py                        
// [7:15 PM, 11/28/2016] Manisha USC: python -m flask run

$(function(){

   console.log("setSillsProfile.js loaded!");
   var user_id = window.location.search.substring(1).split("=")[1]; 

   function set_data(data){
      var allLanguages = jQuery.makeArray(data.languages);
      var selectedLanguages;

      POPULATE_LISTS.populate("languageList",allLanguages);
   }

   $("#go-bar").click(function(){
      var skill = $("#topicBar").val();
      if(skill != ""){
         var tag = "<li class='ui-state-default'>"+skill+"</li>";
         $("#sortable2").append(tag);
         $("#topicBar").val('');   
      }
   });

   GET_USER_DATA = {
      getData:function(user_id){
         var res = null;

         $.ajax({
              type: 'GET',
              url: "http://127.0.0.1:5000/getlanguages",
              data: {userid:user_id},
              dataType: "json",
              crossDomain: true,
              success: set_data
            }).fail(function(){
               alert("Unable to get data");
         });
      }
   }//end of function GET_USER_DATA

// main get use data call
   GET_USER_DATA.getData(user_id);

   POPULATE_LISTS = {
   	populate: function(className, jsonArray){

   		$.each(jsonArray,function(i,lang){
		   	
		   	var listItem = "";
		   	if(className == "languageSelectedList" || className == "fosSelectedList")
		   		listItem = "<li class='ui-state-highlight'>"+ lang +"</li>"
		   	else
		   		listItem = "<li class='ui-state-default'>"+ lang +"</li>"

		   	$(listItem).appendTo("."+className);
		});
   	}
   }// end of function POPULATE_LISTS

   
   BUILD_SELECTED_LIST = {
   	build: function(){
   		var sel_lang_arr = new Array();
   		var selectedJsonOBJ = {};

   		$(".languageSelectedList li").each(function(){
   			sel_lang_arr.push($(this).text());
   		});
   		selectedJsonOBJ["selectedLang"] = sel_lang_arr;

   		return selectedJsonOBJ;
   	} 
   }//end of BUILD_SELECTED_LIST

   $("#collapsebtn").click(function(){
      if($("#collapse-menu").is(":visible")){
        $("#collapseSelection").hide();
      }else{
        $("#collapseSelection").show();
      }
   });

   $("#lets-byob-btn").click(function(){
      $('#results-table').empty();
      $('#filter-table').empty();

      if($("#collapse-menu").is(":visible")){
        $("#collapseSelection").hide();
      }
      var userJSONObj = BUILD_SELECTED_LIST.build();  // This is final user selected languages and FOS object      

      // Reading Advanced search parameters here

      var skill_level_val = $("input:radio[name='skill-level']:checked");
      var result_req_cnt = $("input:text[name='result-req-cnt']").val();

      if(result_req_cnt == ''){
        result_req_cnt = 5;   //default
      }
      //Start of query building

      var skillCnt = userJSONObj.selectedLang.length;

      if(skillCnt == 0){
        $("#collapseSelection").show();
        alert("Please add atleast one skill into the Query Bucket!");
      }

      var queryString = '';

      for(var i = 0 ; i < skillCnt ; i++){
        if(skillCnt == 1){
          queryString += userJSONObj.selectedLang[i];
        }else{
          if(i == 0){
            queryString += '(';
          }

          queryString += userJSONObj.selectedLang[i];

          if(i < skillCnt - 1)
            queryString += ' OR ';

          if(i == skillCnt - 1){
            queryString += ')';
          }
        }
      }

    POPULATE_RESULTS = {
      display: function(objValue){

          var src = '';

          var imageName = ''

          if(objValue.source == "stackoverflow"){
            imageName = "SO.png";
          }else{
            imageName = "Github3.png";
          }

          src += "<tr class = 'result-row'><td class = 'logo-cell'><img src='styles/"+imageName+"' style= 'height:40px; width:40px'></td>";

          var viewTxt = objValue.views;
          if(objValue.views > 1000){
            viewTxt = Math.ceil(viewTxt/1000);
            viewTxt += 'K';
          }

          src += "<td class = 'views-cell'><span style = 'padding-left:10px'>"+ viewTxt +"<span><br> views</td>";
          src += "<td class = 'innerRow-cell'><table class = 'innerRow-table'><tr><td class = 'title-cell'>"+objValue.title+"</td></tr>";
          if(objValue.repo_description != undefined){
            src += "<tr><td class = 'desc-cell'>"+objValue.repo_description+"</td></tr>";
          }
          var tagStr = '';
          if(objValue.other[0] != undefined)
            var tags = objValue.other[0].split(',');
        
          tagStr += "<div class = 'tag-div'>" + objValue.languages +"</div>";
          $.each(tags,function(key,value){
              tagStr += "<div class = 'tag-div'>" + value +"</div>";
              
          });

          src += "<tr><td class = 'tags-cell'>"+tagStr+"</td></tr></table></td>";
          var url = objValue.url;
          src += "<td class = 'go-cell'><a href = '"+url+"' target='_blank'><button type='button' class='btn btn-default' style='width: 40px; color: #006bb3;'><span class='glyphicon glyphicon-circle-arrow-right'></span></button></a></td></tr>";

          $(src).appendTo("#results-table");

      } 
     }//end of BUILD_SELECTED_LIST


      // solr query code

      $.ajax({
        'url': 'http://localhost:8983/solr/byob/select',
        'data': {'wt':'json','indent':'true', 'q':"languages: " + queryString,'group' : 'true','group.field' : 'groupbycol', 'group.limit' : result_req_cnt, 'group.sort' : 'view_rank asc'},
        'dataType': 'jsonp',
        'jsonp': 'json.wrf'
      }).done(function(data){
        
        // populate results fields from here

        //populated filters here 
        $("<tr class = 'single-filter-cell'><td><button type='button' class='btn btn-default filterbtn' style='width: 150px; color: #006bb3;'>All<span class='glyphicon glyphicon-chevron-right' style='float:right;'></span></button></td></tr>").appendTo("#filter-table");
        $.each(userJSONObj.selectedLang,function(key,skill){
          
          //code to make first letter upeercase
          skill = skill.toLowerCase().replace(/\b[a-z]/g, function(letter) {
                      return letter.toUpperCase();
                  });

          var filter_html_str = "<tr class = 'single-filter-cell'><td><button type='button' class='btn btn-default filterbtn' style='width: 150px; color: #006bb3;'>" + skill +"<span class='glyphicon glyphicon-chevron-right' style='float:right;'></span></button></td></tr>";
          $(filter_html_str).appendTo("#filter-table");
        });

        var allObjs = data.grouped.groupbycol.groups;

        $(allObjs).each(function(key, oneObj){
            var results = oneObj.doclist.docs;

            
            $(results).each(function(key,singleObj){
                POPULATE_RESULTS.display(singleObj);
              });

        });
        
        // Filter logic

        $(".filterbtn").click(function(e){
          var filter_type = $(e.target).text();
          console.log(filter_type);
          
          $('#results-table').empty();

          $(allObjs).each(function(key,res){
              var category = res.groupValue;
              var so_option = 'stackoverflow-'+filter_type.toLowerCase();
              var git_option = 'github-'+filter_type.toLowerCase();

              if(category == so_option || category == git_option){

                $(res.doclist.docs).each(function(key,singleObj){
                  POPULATE_RESULTS.display(singleObj);
                });

              }else if(filter_type == "All"){
                $(allObjs).each(function(key, oneObj){
                    var results = oneObj.doclist.docs;

                    $(results).each(function(key,singleObj){
                        POPULATE_RESULTS.display(singleObj);
                    });
                });
              }
            });
        });
      });
   });

  

   $("#topicBar").keyup(function() {
       searchSuggest();
    });

    function searchSuggest() {
    var topicsList = ["1c enterprise", "abap", "actionscript", "ada", "agda", "ags script", "alloy", "ampl", "antlr", "apacheconf", "apex", "api blueprint", "apl", "applescript", "arc", "arduino", "asp", "aspectj", "assembly", "ats", "augeas", "autohotkey", "autoit", "awk", "batchfile", "befunge", "bison", "bitbake", "blitzbasic", "blitzmax", "bluespec", "boo", "brainfuck", "brightscript", "bro", "c", "c#", "c++", "cap'n proto", "cartocss", "ceylon", "chapel", "charity", "chuck", "cirru", "clarion", "clean", "click", "clips", "clojure", "cmake", "cobol", "coffeescript", "coldfusion", "common lisp", "component pascal", "cool", "coq", "crystal", "csound", "csound document", "csound score", "css", "cucumber", "cuda", "cycript", "d", "darcs patch", "dart", "diff", "digital command language", "dm", "dogescript", "graphviz (dot)", "dtrace", "dylan", "e", "eagle", "ec", "ecl", "eiffel", "elixir", "elm", "emacs lisp", "emberscript", "eq", "erlang", "f#", "factor", "fancy", "fantom", "filebench wml", "flux", "forth", "fortran", "freemarker", "frege", "game maker language", "gams", "gap", "gcc machine description", "gdb", "gdscript", "genshi", "gettext catalog", "glsl", "glyph", "gnuplot", "go", "golo", "gosu", "grace", "grammatical framework", "groff", "groovy", "hack", "handlebars", "harbour", "haskell", "haxe", "hcl", "hlsl", "html", "hy", "hyphy", "idl", "idris", "igor pro", "inform 7", "inno setup", "io", "ioke", "isabelle", "j", "jasmin", "java", "javascript", "jflex", "jsoniq", "julia", "jupyter notebook", "kicad", "kit", "kotlin", "krl", "labview", "lasso", "lean", "lex", "lilypond", "limbo", "liquid", "livescript", "llvm", "logos", "logtalk", "lolcode", "lookml", "loomscript", "lsl", "lua", "m", "m4", "makefile", "mako", "markdown", "mask", "mathematica", "matlab", "max", "maxscript", "mercury", "metal", "minid", "mirah", "modelica", "modula-2", "module management system", "monkey", "moocode", "moonscript", "mql4", "mql5", "mtml", "mupad", "myghty", "ncl", "nemerle", "nesc", "netlinx", "netlinx+erb", "netlogo", "newlisp", "nginx", "nimrod", "nit", "nix", "nsis", "nu", "objective-c", "objective-c++", "objective-j", "ocaml", "omgrofl", "ooc", "opa", "opal", "openedge abl", "openscad", "ox", "oxygene", "oz", "pan", "papyrus", "parrot", "pascal", "pawn", "perl", "perl6", "php", "picolisp", "piglatin", "pike", "plpgsql", "plsql", "pogoscript", "pony", "postscript", "pov-ray sdl", "powerbuilder", "powershell", "processing", "prolog", "propeller spin", "protocol buffer", "puppet", "pure data", "purebasic", "purescript", "python", "qmake", "qml", "r", "racket", "ragel in ruby host", "raml", "rdoc", "realbasic", "rebol", "red", "redcode", "ren'py", "renderscript", "rexx", "robotframework", "rouge", "ruby", "runoff", "rust", "saltstack", "sas", "scala", "scheme", "scilab", "self", "shell", "shellsession", "shen", "slash", "smali", "smalltalk", "smarty", "smt", "sourcepawn", "sqf", "sql", "sqlpl", "squirrel", "srecode template", "stan", "standard ml", "stata", "supercollider", "swift", "systemverilog", "tcl", "tea", "terra", "tex", "thrift", "ti program", "tla", "turing", "txl", "typescript", "uno", "unrealscript", "urweb", "vala", "vcl", "verilog", "vhdl", "viml", "visual basic", "volt", "vue", "web ontology language", "webidl", "wisp", "x10", "xbase", "xc", "xml", "xojo", "xpages", "xproc", "xquery", "xs", "xslt", "xtend", "yacc", "zephir", "zimpl"];

   var str = document.getElementById("topicBar").value;
   if (str != "") {
        $("#popups").show();
      document.getElementById("popups").innerHTML = "";
   
      for (var i=0; i<topicsList.length; i++) {
         var thisState = topicsList[i].nodeValue;
   
         if (topicsList[i].toLowerCase().indexOf(str.toLowerCase()) == 0) {
            var tempDiv = document.createElement("div");
            tempDiv.innerHTML = topicsList[i];
            tempDiv.onclick = makeChoice;
            tempDiv.className = "suggestions";
            document.getElementById("popups").appendChild(tempDiv);
         }
      }
      var foundCt = document.getElementById("popups").childNodes.length;
   }
    
    /*********hides popups div on null entry************/
    if (str == "") {
        $("#popups").hide();
    }
}

function makeChoice(evt) {
   var thisDiv = (evt) ? evt.target : window.event.srcElement;
   document.getElementById("topicBar").value = thisDiv.innerHTML;
    $("#popups").hide();
}

});