odoo.define("balance.notidication",function(require){
    const { registry } = require("@web/core/registry");

const myService = {
    dependencies: ["notification"],
    start(env, { notification }) {
        let counter = 1;
        setInterval(() => {
            notification.add(`Tick Tock ${counter++}`);
        }, 5000);
    }
};

registry.category("services").add("myService", myService);



});