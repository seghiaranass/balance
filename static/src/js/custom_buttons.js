odoo.define('balance.tree_view', function (require) {
    "use strict";


    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({
        /**
         * @override
         */
        _renderBody: function () {
            var self = this;
            var $body = this._super.apply(this, arguments);
            var rows = this.state.data;

            _.each(rows, function (row, index) {
                if (row.data.created_datetime < new Date() && row.data.state !== 'paid') {
                    $body.find('tr[data-id="' + row.id + '"]').addClass('bg_danger');
                }
            });

            return $body;
        },
    });
});
