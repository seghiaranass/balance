document.addEventListener("DOMContentLoaded", function () {
    var targetNode = document.querySelector('body');
    var config = { attributes: false, childList: true, subtree: true };

    var processMonths = function() {
        var elements = document.querySelectorAll('div[name="created_datetime"]');
        var lastMonth = null;

        elements.forEach(function(element, index) {

            var monthYear = element.textContent.trim().split('/')[1];

            if (lastMonth !== null && lastMonth !== monthYear) {
                // Add border to the previous item if current month is different
                // elements[index - 1].closest('tr').style.borderBottom = "5px solid black";
                elements[index - 1].closest('tr').classList.add("row_bottom_border")
            }

            if (index === elements.length - 1) {
                element.closest('tr').classList.add("row_bottom_border")
            }

            lastMonth = monthYear;
        });
    };

    var callback = function (mutationsList, observer) {
        for (var mutation of mutationsList) {
            if (mutation.addedNodes.length) {
                var isTargetAdded = false;
                mutation.addedNodes.forEach(function(node) {
                    if (node.classList && node.classList.contains('balance_view_created_datetime')) {
                        isTargetAdded = true;
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
