# OrangeMe ledger slots of the c3 queue
run_condition.sh names the slot `<SLOT>-<CONDITION>` (SLOT=D): every condition has its own isolated OrangeMe ledger. Each is created as a bare-clone of slots/D/ledgers at the pristine state
(slot D's ledgers at their head: chat.git init commit; project.git ff7ed16, which holds the evaluation workspace WS-CA6D7A081C41 registry and memory the sessions require) so no run sees another condition's ledger writes.
Created 2026-10-28 (the queue's first run failed with "git clone failed: repository .../slots/D-RG2-RANDOMIZED/ledgers/chat.git does not exist").
