import Page from "../page.js";
import { $ } from "@wdio/globals";

export class ForwardProxyForm extends Page {
    async setAuthorizationFlow(selector: string) {
        await this.searchSelect(
            '[name="authorizationFlow"]',
            "authorizationFlow",
            `div*=${selector}`,
        );
    }

    get externalHost() {
        return $('>>>input[name="externalHost"]');
    }
}

export default new ForwardProxyForm();
