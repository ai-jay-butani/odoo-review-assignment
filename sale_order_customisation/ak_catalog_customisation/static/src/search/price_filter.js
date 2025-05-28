/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";
import { useState, onWillStart} from "@odoo/owl";
import { SearchPanel } from "@web/search/search_panel/search_panel";

patch(SearchPanel.prototype, {
    setup() {
        super.setup();
        this.priceState = useState({
            minPrice: 0,
            maxPrice: 0,
            minBound: 0,
            maxBound: 0,
        });

        // Use this data to initialize state
        onWillStart(async () => {
            const result = await rpc('/product_catalog/max_price');
            this.priceState.minBound = result.min_price;
            this.priceState.minPrice = result.min_price;
            this.priceState.maxBound = result.max_price;
            this.priceState.maxPrice = result.max_price;
        });
    },
    onMinPriceChange(ev) {
        this.priceState.minPrice = ev.target.value;
        this._updateSearchContext();
    },

    onMaxPriceChange(ev) {
        this.priceState.maxPrice = ev.target.value;
        this._updateSearchContext();
    },

    _updateSearchContext() {
        const min = this.priceState.minPrice;
        const max = this.priceState.maxPrice;

        this.env.searchModel._context.price_filter = {
            minPrice: min,
            maxPrice: max
        };
        this.env.searchModel.search();
    },

},  "ak_catalog_customisation.PriceFilterPatch");
