PYTHON=python

.PHONY: \
	all \
	run \
	discover \
	classify \
	report \
	action-report \
	dashboard \
	snapshot \
	trend \
	init-issues \
	campaign-report \
	update-issue \
	campaign-queue \
	generate-issue \
	auto-priority \
	top-targets \
	campaign-metrics \
	dashboard-data \
	set-priority \
	show-repo \
	high-impact \
	outreach-queue \
	scan \
	status \
	clean

all: scan

scan: discover classify auto-priority report action-report campaign-report campaign-metrics dashboard-data snapshot trend dashboard

status: campaign-metrics top-targets high-impact outreach-queue

run: scan

discover:
	$(PYTHON) scripts/discover.py

classify:
	$(PYTHON) scripts/classify_repos.py

report:
	$(PYTHON) scripts/report.py

action-report:
	$(PYTHON) scripts/action_report.py

dashboard:
	$(PYTHON) scripts/dashboard.py
	cp data/dashboard.html docs/index.html
	cp data/dashboard_data.json docs/dashboard_data.json

snapshot:
	$(PYTHON) scripts/save_snapshot.py

trend:
	$(PYTHON) scripts/trend.py

init-issues:
	$(PYTHON) scripts/init_issues.py

campaign-report:
	$(PYTHON) scripts/campaign_report.py

update-issue:
	$(PYTHON) scripts/update_issue.py

campaign-queue:
	$(PYTHON) scripts/campaign_queue.py

generate-issue:
	$(PYTHON) scripts/generate_issue.py

auto-priority:
	$(PYTHON) scripts/auto_priority.py

top-targets:
	$(PYTHON) scripts/top_targets.py

campaign-metrics:
	$(PYTHON) scripts/campaign_metrics.py

dashboard-data:
	$(PYTHON) scripts/export_dashboard_data.py

set-priority:
	$(PYTHON) scripts/set_priority.py

show-repo:
	$(PYTHON) scripts/show_repo_fields.py

high-impact:
	$(PYTHON) scripts/high_impact.py

outreach-queue:
	$(PYTHON) scripts/outreach_queue.py

clean:
	rm -f data/repos.json
	rm -f data/repos_classified.json
	rm -f data/dashboard.html
	rm -f reports/action_required.md
	rm -f docs/index.html