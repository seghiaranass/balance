odoo.define('your_module_name.list_controller', function(require) {
    "use strict";

    var ListController = require('web.ListController');

    ListController.include({

        renderButtons: function($node) {
            this._super.apply(this, arguments);  // Calls the original button rendering method
            if (this.modelName === 'your.balance.model' && this.buttons) {
                var button = $("<button type='button' class='btn btn-secondary'>Your Button</button>");
                button.click(this.proxy('button_clicked'));
                this.$buttons.append(button);
            }
        },

        button_clicked: function() {
            // Your button action goes here. For instance, calling a server method:
            this._rpc({
                model: 'your.balance.model',
                method: 'your_button_method',
                args: [],
            });
        },
    });
});
