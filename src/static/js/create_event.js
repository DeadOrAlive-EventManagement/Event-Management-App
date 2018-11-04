div_var1 = document.getElementById("first_info");
div_var2 = document.getElementById("second_info");
div_var3 = document.getElementById("third_info");
div_var4 = document.getElementById("forth_info");
div_var5 = document.getElementById("fifth_info");
div_var6 = document.getElementById("sixth_info");


btn_first_next = document.getElementById("first_next");
btn_second_next = document.getElementById("second_next");
btn_third_next = document.getElementById("third_next");
btn_forth_next = document.getElementById("forth_next");
btn_fifth_next = document.getElementById("fifth_next");

btn_second_prev = document.getElementById("second_prev");
btn_third_prev = document.getElementById("third_prev");
btn_forth_prev = document.getElementById("forth_prev");
btn_fifth_prev = document.getElementById("fifth_prev");


btn_first_next.addEventListener("click", doNext1);
obj = {
    stopSubmission: function() {
         'use strict';
         window.addEventListener('load', function() {
         // Fetch all the forms we want to apply custom Bootstrap validation styles to
         var forms = document.getElementsByClassName('needs-validation');
         // Loop over them and prevent submission
         this.console.log("StopSubmission")
         var validation = Array.prototype.filter.call(forms, function(form) {
         form.addEventListener('submit', function(event) {
             if (form.checkValidity() === false) {
                 event.preventDefault();
                 event.stopPropagation();
             }
             form.classList.add('was-validated');
         }, false);
         });
     }, false);
    }
}
obj.stopSubmission();
function checkValid()
{
    alert("checkValid");
    number = document.getElementById("num_people")
    budget= document.getElementById("datepicker")
    date = document.getElementById("budget")
    flag = true;
    if(!number.checkValidity())
    {
        number.setCustomValidity('Please input a valid number.')
        flag = false;
    }    
    else
        number.setCustomValidity('')
    if(!budget.checkValidity())
    {
        budget.setCustomValidity('Please input a valid budget')
        flag = false;
    }    
    else
        budget.setCustomValidity('')
    if(!date.checkValidity())
    {
        date.setCustomValidity('Please input a valid date')
        flag = false;
    }    
    else
        date.setCustomValidity('')
    return flag;
}
function doNext1()
{
    if(checkValid())
    {
        div_var1.setAttribute("style", "display:none");
        div_var2.setAttribute("style", "display:display");
    }
    else{
        myForm = $("#regForm")
        myForm.find(':submit').click();
    }
    

}



btn_second_next.addEventListener("click", doNext2);
function doNext2()
{
    div_var2.setAttribute("style", "display:none");
    div_var3.setAttribute("style", "display:display");

}

btn_second_prev.addEventListener("click", doPrev2);
function doPrev2()
{
    div_var2.setAttribute("style", "display:none");
    div_var1.setAttribute("style", "display:display");

}

btn_third_next.addEventListener("click", doNext3);
function doNext3()
{
    div_var3.setAttribute("style", "display:none");
    div_var4.setAttribute("style", "display:display");

}

btn_third_prev.addEventListener("click", doPrev3);
function doPrev3()
{
    div_var3.setAttribute("style", "display:none");
    div_var2.setAttribute("style", "display:display");

}

btn_forth_next.addEventListener("click", doNext4);
function doNext4()
{
    div_var4.setAttribute("style", "display:none");
    div_var5.setAttribute("style", "display:display");

}

btn_forth_prev.addEventListener("click", doPrev4);
function doPrev4()
{
    div_var4.setAttribute("style", "display:none");
    div_var3.setAttribute("style", "display:display");

}

btn_fifth_next.addEventListener("click", doNext5);
function doNext5()
{
    div_var5.setAttribute("style", "display:none");
    div_var6.setAttribute("style", "display:display");

}

btn_fifth_prev.addEventListener("click", doPrev5);
function doPrev5()
{
    div_var5.setAttribute("style", "display:none");
    div_var4.setAttribute("style", "display:display");

}
