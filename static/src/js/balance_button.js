/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';

export class SaleListController extends ListController {
    setup() {
        super.setup();
    }
    
    async OnTodayClick() {
        // for (const record of this.model.root.records) {
        //     console.log(record.data.created_date_part);
        // }

            const today = new Date().toISOString().slice(0, 10);

            // Assuming you want to filter based on some criteria, e.g., a field named 'state' being 'done'
            const domain = [['created_date_part', '=', today]];

        // Check if the model has a 'load' or 'reload' method to apply the domain and refresh the view
        if (this.model && (this.model.load || this.model.reload)) {
            const params = {
                domain: domain,
                // Add other parameters if needed
            };
            if (this.model.load) {
                await this.model.load(params);
            } else if (this.model.reload) {
                await this.model.reload(params);
            }

            // Refresh the renderer to reflect the changes, if necessary
            if (this.renderer && this.renderer.updateState) {
                this.renderer.updateState({}, { reload: true });
            }
        }
    }


    async OnThisWeekClick() {
        // Get today's date
        const currentDate = new Date();
    
        // Determine the current day of the week (0 = Sunday, 1 = Monday, etc.)
        const currentDay = currentDate.getDay();
    
        // Calculate the start of the week (assuming Sunday as the first day)
        const startOfWeek = new Date(currentDate);
        startOfWeek.setDate(currentDate.getDate() - currentDay);
        
        // Calculate the end of the week (Saturday)
        const endOfWeek = new Date(startOfWeek);
        endOfWeek.setDate(startOfWeek.getDate() + 6);
    
        // Convert dates to YYYY-MM-DD format
        const startWeekStr = startOfWeek.toISOString().slice(0, 10);
        const endWeekStr = endOfWeek.toISOString().slice(0, 10);
    
        // Create a domain filter for records within the current week
        const domain = [
            ['created_date_part', '>', startWeekStr],
            ['created_date_part', '<', endWeekStr]
        ];
    
        // The rest of your function remains the same to apply the domain and refresh the view
        if (this.model && (this.model.load || this.model.reload)) {
            const params = {
                domain: domain,
                // Add other parameters if needed
            };
            if (this.model.load) {
                await this.model.load(params);
            } else if (this.model.reload) {
                await this.model.reload(params);
            }
    
            // Refresh the renderer to reflect the changes, if necessary
            if (this.renderer && this.renderer.updateState) {
                this.renderer.updateState({}, { reload: true });
            }
        }
    }
    async OnNextWeekClick() {
        // Get today's date
        const currentDate = new Date();
    
        // Determine the current day of the week (0 = Sunday, 1 = Monday, etc.)
        const currentDay = currentDate.getDay();
    
        // Calculate the start of the next week (assuming Sunday as the first day)
        const startOfNextWeek = new Date(currentDate);
        startOfNextWeek.setDate(currentDate.getDate() - currentDay + 7);
    
        // Calculate the end of the next week (Saturday)
        const endOfNextWeek = new Date(startOfNextWeek);
        endOfNextWeek.setDate(startOfNextWeek.getDate() + 6);
    
        // Convert dates to YYYY-MM-DD format
        const startNextWeekStr = startOfNextWeek.toISOString().slice(0, 10);
        const endNextWeekStr = endOfNextWeek.toISOString().slice(0, 10);
    
        // Create a domain filter for records within the next week
        const domain = [
            ['created_date_part', '>=', startNextWeekStr],
            ['created_date_part', '<=', endNextWeekStr]
        ];
    
        // The rest of your function remains the same to apply the domain and refresh the view
        if (this.model && (this.model.load || this.model.reload)) {
            const params = {
                domain: domain,
                // Add other parameters if needed
            };
            if (this.model.load) {
                await this.model.load(params);
            } else if (this.model.reload) {
                await this.model.reload(params);
            }
    
            // Refresh the renderer to reflect the changes, if necessary
            if (this.renderer && this.renderer.updateState) {
                this.renderer.updateState({}, { reload: true });
            }
        }
    }
    async OnThisMonthClick() {
        // Get today's date
        const currentDate = new Date();
    
        // Calculate the first day of the current month
        const startOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    
        // Calculate the last day of the current month
        // Set the day to 0 of the next month will give you the last day of the current month
        const endOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    
        // Convert dates to YYYY-MM-DD format
        const startOfMonthStr = startOfMonth.toISOString().slice(0, 10);
        const endOfMonthStr = endOfMonth.toISOString().slice(0, 10);
    
        // Create a domain filter for records within the current month
        const domain = [
            ['created_date_part', '>=', startOfMonthStr],
            ['created_date_part', '<=', endOfMonthStr]
        ];
    
        // The rest of your function remains the same to apply the domain and refresh the view
        if (this.model && (this.model.load || this.model.reload)) {
            const params = {
                domain: domain,
                // Add other parameters if needed
            };
            if (this.model.load) {
                await this.model.load(params);
            } else if (this.model.reload) {
                await this.model.reload(params);
            }
    
            // Refresh the renderer to reflect the changes, if necessary
            if (this.renderer && this.renderer.updateState) {
                this.renderer.updateState({}, { reload: true });
            }
        }
    }
    
    async OnNextMonthClick() {
        // Get today's date
        const currentDate = new Date();
    
        // Calculate the first day of the next month
        const startOfNextMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
    
        // Calculate the last day of the next month
        const endOfNextMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 2, 0);
    
        // Convert dates to YYYY-MM-DD format
        const startOfNextMonthStr = startOfNextMonth.toISOString().slice(0, 10);
        const endOfNextMonthStr = endOfNextMonth.toISOString().slice(0, 10);
    
        // Create a domain filter for records within the next month
        const domain = [
            ['created_date_part', '>=', startOfNextMonthStr],
            ['created_date_part', '<=', endOfNextMonthStr]
        ];
    
        // The rest of your function remains the same to apply the domain and refresh the view
        if (this.model && (this.model.load || this.model.reload)) {
            const params = {
                domain: domain,
                // Add other parameters if needed
            };
            if (this.model.load) {
                await this.model.load(params);
            } else if (this.model.reload) {
                await this.model.reload(params);
            }
    
            // Refresh the renderer to reflect the changes, if necessary
            if (this.renderer && this.renderer.updateState) {
                this.renderer.updateState({}, { reload: true });
            }
        }
    }
    
}

registry.category("views").add("button_in_tree", {
    ...listView,
    Controller: SaleListController,
    buttonTemplate: "balance_button.ListView.Buttons",
});
