# November 2026 methane factor plausibility review

Run: `202611-monthly`. The immutable report used live public GET pagination to an empty terminal page on 2 November 2026. Snapshot SHA-256: `57670b175002cdb9a113f9ad860b85e15695d5b8468c57214d763412ad4945c4`. Raw snapshot and mail receipt remain ignored locally.

## Results and limits

| Assessment | Result |
|---|---:|
| Database records | 183 |
| Category/unit groups | 44 |
| Numerical consistency prompts | 0 |
| Statistical peer signals | 0 |
| Broad contextual magnitude contrasts | 12 |
| Stored statistics without sufficient usable peer references | 223 |

These results do not establish that every factor is plausible or independently verified. The last count describes statistics, not distinct records. All nine PNG comparison pages were visually inspected. The self-contained [HTML report](report.html) embeds all plots and provides exact values, source links and provenance; [audit.json](audit.json) retains original and normalized statistics. Blank plotted rows do not mean zero emissions.

## Useful investigation priorities

1. **Aquatic pathways and near-zero ratios:** rows 158 and 160 create a very large ratio because the denominator is near zero. The [existing aquatic synthesis](../../../wiki/papers/an-assessment-of-co2-and-ch4-emissions-in-a-tropical-river-from-the-kenyir-reservoir-to-the-est-215a71ff.md) identifies the small wet-season reservoir value as ebullition, distinct from diffusive estimates elsewhere. Compare pathway, location, season, gas-transfer assumptions and sampling duration before considering any deeper investigation; the ratio alone is not evidence of error.
2. **Peatland statistics and area boundaries:** inspect soil chambers versus ditch water-surface fluxes and plantation-area upscaling before pooling rows 144–154 and 164–168. Check the literal source statistic (mean/median/range), carbon versus methane mass and SE versus SD. The [ditch](../../../wiki/papers/greenhouse-gas-emissions-from-ditches-in-oil-palm-plantations-on-tropical-peatlands-in-malaysia-13fd082f.md), [nitrogen](../../../wiki/papers/long-term-effects-of-nitrogen-fertilization-on-methane-emissions-in-drained-tropical-peatland-d804c119.md) and [microbial](../../../wiki/papers/temporal-dynamics-of-soil-microbial-c-and-n-cycles-with-ghg-fluxes-in-the-transition-from-tropi-3a6e2e0c.md) notes preserve relevant limitations and source locations. This is an interpretation check, not a proposed database correction.
3. **Oil/gas process boundaries:** venting, flaring, processing and production/upgrading describe different processes even within a category. Keep sales-volume denominators separate from energy-normalized factors. Consult the [source synthesis](../../../wiki/papers/development-of-tier-2-fugitive-emission-factors-for-malaysia-s-oil-and-gas-systems-3c96f098.md) for measured inputs, engineering assumptions and normal-operation coverage.
4. **Independent comparison coverage:** obtain comparable studies with matching country, condition, statistic, method and boundary before treating a contrast as a peer outlier. Different DOIs or paper titles do not guarantee independent data.

IPCC/BUR defaults stored only in `min` retain the owner's accepted point-factor convention. Differences across fuels, animal species and technologies are contextual contrasts. Q01's accepted conversion difference and Q02's resolved paddy issue remain closed; this audit does not reopen them. No values, units, conditions, scientific verification flags or database records were changed.
