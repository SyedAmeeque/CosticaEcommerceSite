var item_box_checked = document.querySelectorAll('.item_box_checked');
var checkbox_selected_length = document.querySelector('.checkbox_selected_length');
// alert(checkbox_selected_length);
item_box_checked.forEach((box) =>{
    box.addEventListener('change', function(){
        if(box.checked){
         checkbox_selected_length.innerHTML = Array.from(item_box_checked).filter(box => box.checked).length;       
        }else{
          checkbox_selected_length.innerHTML = Array.from(item_box_checked).filter(box => box.checked).length;
        }
    })
});

var select_all_checkbox_btn = document.getElementById('select_all');
select_all_checkbox_btn.addEventListener('click', function() {
item_box_checked.forEach((box) => {
    box.checked = !box.checked;
});

if (select_all_checkbox_btn.innerText === 'Select All') {
    select_all_checkbox_btn.innerText = 'Deselect All';
} else {
    select_all_checkbox_btn.innerText = 'Select All';
}

checkbox_selected_length.innerHTML = Array.from(item_box_checked).filter(box => box.checked).length;
});

var checkout_form = document.getElementById('checkout_form');
var checkout_ids_list = document.getElementById('checkout_ids_list');
checkout_form.addEventListener('submit', function() {
    var checkedValues = Array.from(item_box_checked)
    .filter(box => box.checked)
    .map(box => box.value);

    var idsString = checkedValues.join(','); // Join values with commas

    checkout_ids_list.value = idsString;
});

      


function terms_and_condition_btn(){
    var box = document.getElementById('term_checked');
    if(box.checked){
    checkout_btn.disabled = false;
    }else{
    checkout_btn.disabled = true;
    }
};
    
   

  
function order_form_submit(){
    var order_form = document.getElementById('order_form');
    order_form.submit();
};

    

