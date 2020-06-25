$(document).ready(function () {
    $('#dataTable').DataTable();
    myscript.init();
});

function Highlight_Sentence(index, total_sentence) {
    for (var i = 1; i < (total_sentence - 1) ; i++) {
        var str = "mtapds-pos" + i;
        document.getElementById(str).style.backgroundColor = "";
        str = "mtapds-repli" + i;
        document.getElementById(str).style.backgroundColor = "";
    }
    $.ajax({
        url: '/QLDoc/ReAssign',
        data: { index: index },
        success: function (response) {
            //console.log(response);
        }
    });
    document.getElementById("mtapds-pos" + index).style.backgroundColor = "yellow";
    document.getElementById("mtapds-repli" + index).style.backgroundColor = "yellow";
	$("#sentence-redirect").val(index);

}


var myscript = {
    init: function () {
        var me = this;
        me.selectDocxA('.first-docx');
        me.selectDocxB('.second-docx');
    },
    selectDocxA: function (selectId) {
        $.ajax({
            url: '/QLDoc/Doc_HtmlA',
            data: {},
            success: function (response) {
                $(selectId).html(response);
            }
        });
    },
    selectDocxB: function (selectId) {
        $.ajax({
            url: '/QLDoc/Doc_HtmlB',
            data: {},
            success: function (response) {
                $(selectId).html(response);
            }
        });
    }
};
var href_obj = {
    next_func: function (total_sen) {
        $.ajax({
            url: '/QLDoc/HrefIndexNext',
            data: {},
            success: function (response) {
                //console.log(response);
                var i;
                for (i = 1; i < total_sen; i++) {
                    var str = "mtapds-pos" + i;
                    document.getElementById(str).style.backgroundColor = "";
                    str = "mtapds-repli" + i;
                    document.getElementById(str).style.backgroundColor = "";
                }
                location.href = "#mtapds-pos" + response;
                document.getElementById("mtapds-pos" + response).style.backgroundColor = "yellow";
                location.href = "#mtapds-repli" + response;
                document.getElementById("mtapds-repli" + response).style.backgroundColor = "yellow";
                //$("#sentence-redirect").val(response);
            }
        });
    },
    prev_func: function (total_sen) {
        $.ajax({
            url: '/QLDoc/HrefIndexPrev',
            data: {},
            success: function (response) {
                //console.log(response);
                var i;
                for (i = 1; i < total_sen; i++) {
                    var str = "mtapds-pos" + i;
                    document.getElementById(str).style.backgroundColor = "";
                    str = "mtapds-repli" + i;
                    document.getElementById(str).style.backgroundColor = "";
                }
                location.href = "#mtapds-pos" + response;
                document.getElementById("mtapds-pos" + response).style.backgroundColor = "yellow";
                location.href = "#mtapds-repli" + response;
                document.getElementById("mtapds-repli" + response).style.backgroundColor = "yellow";
                //$("#sentence-redirect").val(response);
            }
        });
    }
}