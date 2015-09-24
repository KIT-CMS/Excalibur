#include "ZJetTypes.h"

class ValidZllJetsProducer : public ZJetProducerBase
{
  public:
    ValidZllJetsProducer() : ZJetProducerBase(), minZllJetDeltaRVeto(0) {}

    void Init(ZJetSettings const& settings);

    virtual std::string GetProducerId() const override;

    virtual void Produce(ZJetEvent const& event,
                         ZJetProduct& product,
                         ZJetSettings const& settings) const override;

  private:
    float minZllJetDeltaRVeto;
};
