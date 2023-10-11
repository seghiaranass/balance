
let processAllTableRows = (elements)=>{
    console.log(elements);
    var lastMonth = null;

    elements.forEach(function(element, index) {

        var monthYear = element.textContent.trim().split('/')[1];

        if (lastMonth !== null && lastMonth !== monthYear) {
            // Add border to the previous item if current month is different
            // elements[index - 1].closest('tr').style.borderBottom = "5px solid black";
            // elements[index - 1].closest('tr').classList.add("row_bottom_border")
            elements[index - 1].closest('tr').classList.add("row_bottom_border")
        }

        if (index === elements.length - 1) {
            element.closest('tr').classList.add("row_bottom_border")
        }

        lastMonth = monthYear;
    });
}



document.addEventListener("DOMContentLoaded", function () {
    var targetNode = document.querySelector('body');
    var config = { attributes: false, childList: true, subtree: true };
    let is_balance = is_facture = false;
    var processMonths = function() {
        var elements;
        if(is_balance){
             elements = document.querySelectorAll('div[name="created_datetime"]');
             is_balance = false;
        }else if(is_facture){
             elements = document.querySelectorAll('td[name="invoice_date"]');
            let factureNextBtn =  document.querySelector('button[aria-label="Next"]')
            console.log("Hello");
            if(factureNextBtn)
                factureNextBtn.addEventListener('click',()=>{
                    console.log("Clicked");
                    let elements_ = document.querySelectorAll('td[name="invoice_date"]');
                    processAllTableRows(elements_);
            })

             is_facture = false;
        }

        processAllTableRows(elements);
        
    };

    var callback = function (mutationsList, observer) {
        is_balance = is_facture = false;
        for (var mutation of mutationsList) {
            if (mutation.addedNodes.length) {
                var isTargetAdded = false;
                mutation.addedNodes.forEach(function(node) {

                    if(node.classList && node.classList.contains('balance_view_created_datetime')){
                        isTargetAdded = true;
                        is_balance = true;
                    }
                    if(node.classList && node.classList.contains('facture_client_view_bottom')){
                        isTargetAdded = true;
                        is_facture = true;
                    }


                });

                if (isTargetAdded) {
                    processMonths();
                }
            }
        }
    };

    var observer = new MutationObserver(callback);
    observer.observe(targetNode, config);
});
