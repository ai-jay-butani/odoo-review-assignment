/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";

patch(ProductCatalogKanbanModel.prototype,  {
    async _loadData(params) {
        const priceFilter = this.env.searchModel._context?.price_filter;
        const min = priceFilter?.minPrice || 0 ;
        const max = priceFilter?.maxPrice || 0 ;
        const baseDomain = params.domain || [];
        const priceDomain = [];

        if (max > min) {
            priceDomain.push(["list_price", ">=", min]);
            priceDomain.push(["list_price", "<=", max]);
        }

        params.domain = [...baseDomain, ...priceDomain];
        return await super._loadData(params);
    }

});