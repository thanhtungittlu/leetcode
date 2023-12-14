from mobio.libs.dyn.models.mongo import MerchantConfigStructure


class MerchantConfigHelper:
    def update_merchant_config(self, merchant_config, current_version):
        while merchant_config.get(MerchantConfigStructure.VERSION) < current_version:
            if merchant_config.get(MerchantConfigStructure.VERSION) == 0.1:
                merchant_config = self.update_v0dot1_to_v0dot2(merchant_config)
        return merchant_config

    def update_v0dot1_to_v0dot2(self, merchant_config):
        merchant_config[MerchantConfigStructure.VERSION] = 0.2
        merchant_config['field_template'] = 1
        merchant_config[MerchantConfigStructure.DYNAMIC_FIELDS] = []
        return merchant_config
