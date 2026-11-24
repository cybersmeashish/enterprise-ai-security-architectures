import json, math, sys, unittest
from dataclasses import replace
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"lab"))
from core import capacity,generation_cost,clause_chunks,authorised,redact_synthetic,CacheScope,ScopedSemanticCache,route_model,bounded_tool_plan,parse_answer,safe_envelope

class PlanningTests(unittest.TestCase):
    def setUp(self):self.cfg=json.loads((ROOT/"fixtures/capacity.json").read_text())
    def test_document_page_units(self):
        r=capacity(self.cfg);self.assertAlmostEqual(r["documents_per_second"],100_000_000/(30*86400));self.assertEqual(r["pages_per_month"],600_000_000)
    def test_retry_amplification_changes_workers_not_unique_documents(self):
        a=capacity(self.cfg);c=dict(self.cfg,retry_amplification=1);v=capacity(c)
        self.assertGreater(a["ocr_workers_average"],v["ocr_workers_average"]);self.assertEqual(a["documents_per_second"],v["documents_per_second"])
    def test_capture_schedule_is_separate(self):
        a=capacity(self.cfg);c=dict(self.cfg,capture_hours_per_day=8);v=capacity(c)
        self.assertGreater(v["scanner_stations_assumed_schedule"],a["scanner_stations_assumed_schedule"]);self.assertEqual(v["ocr_workers_average"],a["ocr_workers_average"])
    def test_page_sensitivity(self):
        a=capacity(self.cfg);v=capacity(dict(self.cfg,pages_per_document=12));self.assertEqual(v["pages_per_second"],2*a["pages_per_second"])
    def test_storage_units_and_copies(self):
        r=capacity(self.cfg);self.assertEqual(r["original_images_TB_one_copy"],300);self.assertAlmostEqual(r["vectors_TB_with_factor_and_copies"],4.17792)
    def test_invalid_planning_inputs(self):
        for patch in ({"documents":True},{"worker_utilisation":2},{"capture_days":31},{"pages_per_document":math.nan},{"retry_amplification":0.5},{"copies":1.5}):
            with self.subTest(patch=patch),self.assertRaises(ValueError):capacity(dict(self.cfg,**patch))
    def test_cost_has_no_quality_claim(self):
        r=generation_cost(json.loads((ROOT/"fixtures/cost-scenario.json").read_text()));self.assertAlmostEqual(r["baseline_generation_cost"],35.5);self.assertGreater(r["generation_saving_fraction"],0.7);self.assertFalse(r["quality_verified"])
    def test_invalid_cost_fractions(self):
        c=json.loads((ROOT/"fixtures/cost-scenario.json").read_text())
        with self.assertRaises(ValueError):generation_cost(dict(c,cache_hit_fraction=1.1))

class ChunkAndPrivacyTests(unittest.TestCase):
    def test_clause_provenance_survives_split(self):
        d=json.loads((ROOT/"fixtures/legal-contract.json").read_text());rows=clause_chunks(d,40,5)
        self.assertGreater(len(rows),3)
        for r in rows:self.assertEqual(r["scope"],d["scope"]);self.assertTrue(r["pages"]);self.assertLessEqual(len(r["text"].split()),40)
        self.assertNotIn("cure period following",rows[0]["text"])
    def test_chunk_overlap_bounds(self):
        d=json.loads((ROOT/"fixtures/legal-contract.json").read_text())
        with self.assertRaises(ValueError):clause_chunks(d,10,10)
    def test_cross_case_grant_denied(self):
        r={"bank":"SYN","case":"A","purpose":"support","epoch":3};g=dict(r,verified=True)
        self.assertTrue(authorised(r,g));self.assertFalse(authorised(r,dict(g,case="B")))
    def test_unverified_revoked_or_old_epoch_denied(self):
        r={"bank":"SYN","case":"A","purpose":"support","epoch":3};g=dict(r,verified=True)
        self.assertFalse(authorised(dict(r,revoked=True),g));self.assertFalse(authorised(r,dict(g,epoch=4)));self.assertFalse(authorised(r,dict(g,verified=False)))
    def test_missing_authority_fields_denied(self):
        self.assertFalse(authorised({}, {"verified":True}));self.assertFalse(authorised({"bank":"SYN","case":"A","purpose":"support","epoch":True},{"bank":"SYN","case":"A","purpose":"support","epoch":True,"verified":True}))
    def test_synthetic_pii_patterns(self):
        r=redact_synthetic("SYN: example@example.test PAN ABCDE1234F ID 1111 2222 3333")
        self.assertNotIn("ABCDE1234F",r["text"]);self.assertNotIn("example@example.test",r["text"]);self.assertEqual(sum(r["matches"].values()),3)
    def test_redaction_does_not_claim_completeness(self):
        r=redact_synthetic("Unrecognised synthetic name and image")
        self.assertFalse(r["complete_pii_detection"])

class CacheTests(unittest.TestCase):
    def setUp(self):
        self.scope=CacheScope("SYN","employee1","A","support",3,"c1","r1","en","2026-11-24")
        self.cache=ScopedSemanticCache();self.cache.put(self.scope,"notice",["45","not-cancelled"],"synthetic answer",100)
    def hit(self,scope=None,**kwargs):
        p={"scope":scope or self.scope,"intent":"notice","important_values":["45","not-cancelled"],"similarity":0.99,"now":50,"eligible":True,"grants_current":True};p.update(kwargs);return self.cache.get(**p)
    def test_same_scope_valid_hit(self):self.assertEqual(self.hit(),"synthetic answer")
    def test_another_subject_case_cannot_hit(self):
        self.assertIsNone(self.hit(replace(self.scope,subject_group="employee2")));self.assertIsNone(self.hit(replace(self.scope,case="B")))
    def test_epoch_corpus_release_changes_block(self):
        for s in [replace(self.scope,permission_epoch=4),replace(self.scope,corpus_version="c2"),replace(self.scope,release="r2")]:self.assertIsNone(self.hit(s))
    def test_entities_negation_intent_must_match(self):
        self.assertIsNone(self.hit(important_values=["30","cancelled"]));self.assertIsNone(self.hit(intent="payment"))
    def test_expired_and_revoked_block(self):self.assertIsNone(self.hit(now=101));self.assertIsNone(self.hit(grants_current=False))
    def test_similarity_is_not_permission(self):self.assertIsNone(self.hit(replace(self.scope,purpose="audit"),similarity=1))
    def test_hit_rate_denominators(self):
        self.hit();self.hit(eligible=False);self.hit(similarity=0.1)
        m=self.cache.metrics();self.assertEqual(m["hit_rate_total"],1/3);self.assertEqual(m["hit_rate_eligible"],1/2)
    def test_unverified_cache_flags_rejected(self):
        with self.assertRaises(ValueError):self.hit(grants_current="yes")
    def test_nonfinite_similarity_rejected(self):
        with self.assertRaises(ValueError):self.hit(similarity=math.nan)

class RoutingAndAgentTests(unittest.TestCase):
    def route(self,**kw):
        v={"permitted":True,"supported_language":True,"evidence_sufficient":True,"material":False,"conflict":False,"ocr_uncertain":False};v.update(kw);return route_model(**v)
    def test_router_never_escalates_denial(self):self.assertEqual(self.route(permitted=False,material=True),"deny")
    def test_router_escalates_uncertainty_or_missing_evidence(self):
        self.assertEqual(self.route(),"cheap");self.assertEqual(self.route(ocr_uncertain=True),"smart_or_human_review");self.assertEqual(self.route(evidence_sufficient=False),"human_review")
    def test_router_rejects_model_written_strings(self):
        with self.assertRaises(ValueError):self.route(permitted="yes")
    def test_loop_stops_same_state_and_arguments(self):
        a={"tool":"lookup","args":{"id":"SYN1"},"state_version":1};r=bounded_tool_plan([a,a],{"lookup"});self.assertEqual(r["reason"],"no_progress_loop")
    def test_changed_state_is_not_false_loop(self):
        a={"tool":"lookup","args":{"id":"SYN1"},"state_version":1};r=bounded_tool_plan([a,dict(a,state_version=2)],{"lookup"});self.assertEqual(r["status"],"plan_bounded");self.assertFalse(r["execution"])
    def test_step_budget_and_tool_allowlist(self):
        a={"tool":"lookup","args":{},"state_version":1};self.assertEqual(bounded_tool_plan([a,dict(a,state_version=2)],{"lookup"},1)["reason"],"step_budget");self.assertEqual(bounded_tool_plan([dict(a,tool="send_money")],{"lookup"})["status"],"denied")
    def test_canonical_argument_order_detects_repeat(self):
        a={"tool":"lookup","args":{"a":1,"b":2}};v={"tool":"lookup","args":{"b":2,"a":1}};self.assertEqual(bounded_tool_plan([a,v],{"lookup"})["reason"],"no_progress_loop")

class JsonTests(unittest.TestCase):
    def raw(self,**kw):
        a={"status":"answered","answer":"Synthetic fact","citations":["SYN-D1"],"uncertainty":""};a.update(kw);return json.dumps(a)
    def test_valid_answer(self):self.assertEqual(parse_answer(self.raw(),{"SYN-D1"})["status"],"answered")
    def test_unsupported_citation_rejected(self):
        with self.assertRaises(ValueError):parse_answer(self.raw(citations=["PRIVATE-D2"]),{"SYN-D1"})
    def test_answer_without_evidence_rejected(self):
        with self.assertRaises(ValueError):parse_answer(self.raw(citations=[]),set())
    def test_unknown_fields_or_duplicate_keys_rejected(self):
        for raw in [self.raw(extra="x"),'{"status":"answered","status":"denied"}']:
            with self.assertRaises(ValueError):parse_answer(raw,{"SYN-D1"})
    def test_nonfinite_and_wrong_type_rejected(self):
        for raw in ['{"status":NaN}',self.raw(citations="SYN-D1")]:
            with self.assertRaises(ValueError):parse_answer(raw,{"SYN-D1"})
    def test_invalid_model_text_returns_valid_controlled_error(self):
        a=json.loads(safe_envelope("not JSON",set()));self.assertEqual(a["status"],"error");self.assertEqual(a["citations"],[]);parse_answer(json.dumps(a),set())
    def test_denial_does_not_disclose_citations(self):
        with self.assertRaises(ValueError):parse_answer(self.raw(status="denied"),{"SYN-D1"})
    def test_nontext_provider_response_is_controlled(self):
        self.assertEqual(json.loads(safe_envelope(None,set()))["status"],"error")
    def test_oversized_content_rejected(self):
        with self.assertRaises(ValueError):parse_answer(self.raw(answer="a"*33000),{"SYN-D1"})

if __name__=="__main__":unittest.main()
