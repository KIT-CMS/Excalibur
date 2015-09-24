#include "ZJetTypes.h"

class ValidZllJetsProducer : public ZJetProducerBase
{
  public:
    ValidZllJetsProducer() : ZJetProducerBase(), minZllJetDeltaRVeto(0) {}

    void Init(ZJetSettings const& settings);

    std::string GetProducerId() const override;

    void Produce(ZJetEvent const& event,
                 ZJetProduct& product,
                 ZJetSettings const& settings) const override;

  private:
    float minZllJetDeltaRVeto;
};
