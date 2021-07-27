// Shorthand for $( document ).ready()
// $(function() {
//     $(".toggle").on("click", function(){
//         if($(".item").hasClass("active")){
//             $(".item").removeClass("active");
//         }
//
//         else{
//             $(".item").addClass("active");
//         }
//     })
// });

//
// $(document).ready(function () {
//      $(".menu-toggle").on("click", function(){
//         $('.new-nav').toggleClass('showing');
//         $('.new-nav ul').toggleClass('showing');
//     })
// })

// TO track if user register from mobile or desktop
var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)
if (isMobile){
    var addTextMobile = document.getElementById('mobile');
    document.getElementById("mobile").value = "تم التسجيل من هاتف محمول";
}

else {
    var addTextDesktop = document.getElementById('desktop');
    document.getElementById("desktop").value = "تم التسجيل من جهاز كمبيوتر";
}



// const spinnerBox = document.getElementById('spinner-box')
// const dataBox = document.getElementById('data-box')
//
// $.ajax({
//     type: 'GET',
//     url: '/home/',
//     success: function (response) {
//         setTimeout(()=>{
//             spinnerBox.classList.add('not-visible-spinner')
//             console.log('response', response)
//             for (const item of response){
//                 dataBox.innerHTML += '<b>${item.owner_name}</b>'
//             }
//         }, 500)
//
//     },
//     error: function (error) {
//         setTimeout(()=>{
//             spinnerBox.classList.add('not-visible-spinner')
//             dataBox.innerHTML += '<b>خطأ في التحميل</b>'
//         }, 500)
//     }
// })




// {#    <script>#}
//         {#  make input only number   #}
// {#        function isInputNumber(evt){#}
// {#            var ch = String.fromCharCode(evt.which);#}
// {#            if(!(/[0-9]/.test(ch)) || (/[^\w\-.]/g.test(ch))){#}
// {#                evt.preventDefault();#}
// {#            }#}
// {#        }#}
// {#    </script>#}
//
// {#    <script>#}
//         {#  make input only Text  but must with it blockSpecialRegex func (next script) #}
// {#        function isInputText(evt){#}
// {#            var ch = String.fromCharCode(evt.which);#}
// {#            if((/[0-9]/.test(ch)) || !(/[^\w\-.]/g.test(ch))){#}
// {#                evt.preventDefault();#}
// {#            }#}
// {#        }#}
// {#    </script>#}
//
// {#    <script>#}
//          {##this script to prevent Special char in all input#}
// {#        $('input').on('keypress', function (e) {#}
// {#        var blockSpecialRegex = /[~`!#$%^&()_*؟={}[\]’ـ،"ْْآ؛×÷‘إٌُ:;ُ,ٌ<>ًَ+\/?-]/;#}
// {#          var key = String.fromCharCode(!e.charCode ? e.which : e.charCode);#}
// {#          if(blockSpecialRegex.test(key)){#}
// {#            e.preventDefault();#}
// {#            return false;#}
// {#          }#}
// {#          });#}
// {#    </script>#}
//