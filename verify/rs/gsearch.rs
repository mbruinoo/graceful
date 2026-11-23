// Independent checker for the growth-placement claims of README sections 7, 8, 11, 12, 13.
// Written from the README definitions only (not from src/*.cpp).  Labels are 1..n.
//
//   gsearch solve R B          trees on stdin ("N a-b a-b ..."), one answer per line:
//                              "OK l_0 ... l_{N-1}"  a growth placement whose unused labels never form
//                                                    more than R runs, of which at most B have size >= 2
//                              "NONE"                exhaustive search found none
//   gsearch minskip            per tree: least s such that solve(R=s+1,B=1) succeeds: "S s l_0 ..."
//   gsearch minruns            per tree: least R such that solve(R,B=inf) succeeds:   "R r l_0 ..."
//   gsearch anchors            per tree: a string of N letters, 'A' if the vertex can carry label 1
//   gsearch enum N R B         enumerate every growth placement on N labels within (R,B); per shape:
//                              "T <paren code> <count> <min max-runs> <min skips or 255>", and
//                              "A <paren code>" for every rooted shape seen with the root at label 1
//   gsearch spider N free|zig|level|first   every spider with >= 3 legs on N vertices, centre at label 0
//                              (level, first: the two dealing orders of the README section 13 table):
//                              "legs | OK leg labels ; ..." or "legs | NONE"
//
// Cell-driven search: at the step that places bracket k the program walks over the *unused cells* x
// (cells next to a used cell first), looks at the two cells x+k and x-k, and hangs a still unlabelled
// neighbour of the vertex found there.  Unlabelled neighbours whose hanging branches are isomorphic
// are tried once.  Each tree edge is tried as the top bracket {1,n} in one orientation only
// (reflection i -> n+1-i preserves growth placements, the number of runs and their sizes).

use std::collections::{HashMap, HashSet};
use std::io::{self, BufRead, Write};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

const MAXN: usize = 40;

struct Tree {
    n: usize,
    adj: Vec<Vec<usize>>,
    // bclass[u][i] : isomorphism class of the branch hanging from u through its i-th neighbour
    bclass: Vec<Vec<u32>>,
}

fn branch_code(adj: &Vec<Vec<usize>>, from: usize, to: usize, memo: &mut HashMap<(usize, usize), String>) -> String {
    if let Some(s) = memo.get(&(from, to)) {
        return s.clone();
    }
    let mut kids: Vec<String> = Vec::new();
    for &w in &adj[to] {
        if w != from {
            kids.push(branch_code(adj, to, w, memo));
        }
    }
    kids.sort();
    let s = format!("({})", kids.concat());
    memo.insert((from, to), s.clone());
    s
}

fn make_tree(n: usize, edges: &Vec<(usize, usize)>) -> Tree {
    let mut adj = vec![Vec::new(); n];
    for &(a, b) in edges {
        adj[a].push(b);
        adj[b].push(a);
    }
    let mut memo = HashMap::new();
    let mut ids: HashMap<String, u32> = HashMap::new();
    let mut bclass = vec![Vec::new(); n];
    for u in 0..n {
        for &v in &adj[u] {
            let s = branch_code(&adj, u, v, &mut memo);
            let k = ids.len() as u32;
            let id = *ids.entry(s).or_insert(k);
            bclass[u].push(id);
        }
    }
    Tree { n, adj, bclass }
}

struct Search<'a> {
    t: &'a Tree,
    n: usize,
    full: u64,
    used: u64,
    label: [u8; MAXN],
    at: [u8; MAXN + 2],
    maxruns: u32,
    maxbig: u32,
    nodes: u64,
    budget: u64,
    hit_limit: bool,
}

#[inline]
fn runs_big(unused: u64) -> (u32, u32) {
    let starts = unused & !(unused << 1);
    (starts.count_ones(), (starts & (unused >> 1)).count_ones())
}

impl<'a> Search<'a> {
    fn new(t: &'a Tree, maxruns: u32, maxbig: u32) -> Self {
        let n = t.n;
        Search { t, n, full: ((1u64 << n) - 1) << 1, used: 0, label: [0; MAXN], at: [0; MAXN + 2], maxruns, maxbig, nodes: 0, budget: u64::MAX, hit_limit: false }
    }
    fn put(&mut self, v: usize, l: usize) {
        self.label[v] = l as u8;
        self.at[l] = v as u8;
        self.used |= 1u64 << l;
    }
    fn take(&mut self, v: usize, l: usize) {
        self.label[v] = 0;
        self.used &= !(1u64 << l);
    }
    // place brackets k, k-1, ..., 1
    fn rec(&mut self, k: usize) -> bool {
        if k == 0 {
            return true;
        }
        self.nodes += 1;
        if self.nodes > self.budget {
            self.hit_limit = true;
            return false;
        }
        let unused = self.full & !self.used;
        let (runs_now, _) = runs_big(unused);
        let edge_cells = unused & ((self.used << 1) | (self.used >> 1));
        for pass in 0..2 {
            let mut cells = if pass == 0 { edge_cells } else { unused & !edge_cells };
            if pass == 1 && runs_now + 1 > self.maxruns {
                break; // an interior cell always adds a run
            }
            while cells != 0 {
                let x = cells.trailing_zeros() as usize;
                cells &= cells - 1;
                let (r, b) = runs_big(unused & !(1u64 << x));
                if r > self.maxruns || b > self.maxbig {
                    continue;
                }
                for side in 0..2 {
                    let y = if side == 0 { x + k } else { if x > k { x - k } else { continue } };
                    if y > self.n || (self.used >> y) & 1 == 0 {
                        continue;
                    }
                    let u = self.at[y] as usize;
                    let deg = self.t.adj[u].len();
                    for i in 0..deg {
                        let v = self.t.adj[u][i];
                        if self.label[v] != 0 {
                            continue;
                        }
                        let c = self.t.bclass[u][i];
                        let mut dup = false;
                        for j in 0..i {
                            if self.label[self.t.adj[u][j]] == 0 && self.t.bclass[u][j] == c {
                                dup = true;
                                break;
                            }
                        }
                        if dup {
                            continue;
                        }
                        self.put(v, x);
                        if self.rec(k - 1) {
                            return true;
                        }
                        self.take(v, x);
                        if self.hit_limit {
                            return false;
                        }
                    }
                }
            }
        }
        false
    }
}

// roots: list of (vertex labelled 1, vertex labelled n) to try.
// Returns Some(labels) or None (exhaustive).  Budgets are doubled until an answer is certain.
fn solve_roots(t: &Tree, roots: &Vec<(usize, usize)>, maxruns: u32, maxbig: u32) -> Option<Vec<u8>> {
    let n = t.n;
    if n == 1 {
        return Some(vec![1]);
    }
    let mut budget: u64 = 2000;
    let mut alive: Vec<bool> = vec![true; roots.len()];
    loop {
        let mut any_limit = false;
        for (ri, &(a, b)) in roots.iter().enumerate() {
            if !alive[ri] {
                continue;
            }
            let mut s = Search::new(t, maxruns, maxbig);
            s.budget = budget;
            s.put(a, 1);
            s.put(b, n);
            // moment after the top bracket: unused = 2..n-1, one run
            let (r, bg) = runs_big(s.full & !s.used);
            if r > maxruns || bg > maxbig {
                alive[ri] = false;
                continue;
            }
            if s.rec(n - 2) {
                return Some(s.label[..n].to_vec());
            }
            if s.hit_limit {
                any_limit = true;
            } else {
                alive[ri] = false;
            }
        }
        if !any_limit {
            return None;
        }
        budget = budget.saturating_mul(8);
    }
}

fn edge_roots(t: &Tree) -> Vec<(usize, usize)> {
    // one orientation per edge, one edge per automorphism class {class(u->v), class(v->u)}
    let mut seen: HashSet<(u32, u32)> = HashSet::new();
    let mut out = Vec::new();
    for u in 0..t.n {
        for (i, &v) in t.adj[u].iter().enumerate() {
            if u < v {
                let cu = t.bclass[u][i];
                let j = t.adj[v].iter().position(|&w| w == u).unwrap();
                let cv = t.bclass[v][j];
                let key = if cu < cv { (cu, cv) } else { (cv, cu) };
                if seen.insert(key) {
                    out.push((u, v));
                }
            }
        }
    }
    out
}

fn parse_tree(line: &str) -> Option<Tree> {
    let mut it = line.split_whitespace();
    let n: usize = it.next()?.parse().ok()?;
    let mut edges = Vec::new();
    for tok in it {
        let mut p = tok.split('-');
        let a: usize = p.next()?.parse().ok()?;
        let b: usize = p.next()?.parse().ok()?;
        edges.push((a, b));
    }
    assert!(edges.len() + 1 == n, "bad tree line");
    Some(make_tree(n, &edges))
}

fn fmt_labels(l: &Vec<u8>) -> String {
    l.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" ")
}

fn answer(mode: &str, r: u32, b: u32, t: &Tree) -> String {
    match mode {
        "solve" => match solve_roots(t, &edge_roots(t), r, b) {
            Some(l) => format!("OK {}", fmt_labels(&l)),
            None => "NONE".to_string(),
        },
        "minskip" => {
            let roots = edge_roots(t);
            for s in 0..(t.n as u32) {
                if let Some(l) = solve_roots(t, &roots, s + 1, 1) {
                    return format!("S {} {}", s, fmt_labels(&l));
                }
            }
            "S none".to_string()
        }
        "minruns" => {
            let roots = edge_roots(t);
            for rr in 1..(t.n as u32 + 1) {
                if let Some(l) = solve_roots(t, &roots, rr, u32::MAX) {
                    return format!("R {} {}", rr, fmt_labels(&l));
                }
            }
            "R none".to_string()
        }
        "anchors" => {
            let mut s = String::new();
            for a in 0..t.n {
                // label 1 on a; the top bracket goes to one neighbour per branch class
                let mut roots = Vec::new();
                let mut seen = HashSet::new();
                for (i, &v) in t.adj[a].iter().enumerate() {
                    if seen.insert(t.bclass[a][i]) {
                        roots.push((a, v));
                    }
                }
                s.push(if solve_roots(t, &roots, u32::MAX, u32::MAX).is_some() { 'A' } else { '-' });
            }
            s
        }
        _ => panic!("unknown mode"),
    }
}

fn run_stream(mode: &'static str, r: u32, b: u32, threads: usize) {
    // read in chunks, solve chunk in parallel, print in input order
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut out = io::BufWriter::new(stdout.lock());
    let mut lines = stdin.lock().lines();
    loop {
        let mut chunk: Vec<String> = Vec::new();
        while chunk.len() < 65536 {
            match lines.next() {
                Some(Ok(l)) => {
                    if !l.trim().is_empty() {
                        chunk.push(l)
                    }
                }
                _ => break,
            }
        }
        if chunk.is_empty() {
            break;
        }
        let chunk = Arc::new(chunk);
        let next = Arc::new(AtomicUsize::new(0));
        let mut handles = Vec::new();
        for _ in 0..threads {
            let chunk = chunk.clone();
            let next = next.clone();
            handles.push(std::thread::spawn(move || {
                let mut res: Vec<(usize, String)> = Vec::new();
                loop {
                    let i = next.fetch_add(1, Ordering::Relaxed);
                    if i >= chunk.len() {
                        break;
                    }
                    let t = parse_tree(&chunk[i]).expect("parse");
                    res.push((i, answer(mode, r, b, &t)));
                }
                res
            }));
        }
        let mut all: Vec<(usize, String)> = Vec::new();
        for h in handles {
            all.extend(h.join().unwrap());
        }
        all.sort();
        for (_, s) in all {
            writeln!(out, "{}", s).unwrap();
        }
    }
}

// ---------------------------------------------------------------- enumeration of placements

// code of a rooted tree as a bit string "1 children 0", children sorted; (len, bits)

struct Enum {
    n: usize,
    full: u64,
    maxruns: u32,
    maxbig: u32,
    used: u64,
    ea: [u8; MAXN], // edges in order of placement
    eb: [u8; MAXN],
    ne: usize,
    shapes: HashMap<u64, (u64, u8, u8)>,
    anchors: HashSet<u64>,
    total: u64,
}

fn code_rooted(n: usize, nbr: &Vec<Vec<u8>>, root: usize) -> u64 {
    // iterative: order by BFS, then fold from the leaves
    let mut parent = [255u8; MAXN + 2];
    let mut order = [0u8; MAXN + 2];
    let mut cnt = 1;
    order[0] = root as u8;
    parent[root] = root as u8;
    let mut i = 0;
    while i < cnt {
        let v = order[i] as usize;
        i += 1;
        for &w in &nbr[v] {
            if w != parent[v] {
                parent[w as usize] = v as u8;
                order[cnt] = w;
                cnt += 1;
            }
        }
    }
    debug_assert!(cnt == n);
    let mut bits = [0u64; MAXN + 2];
    let mut len = [0u8; MAXN + 2];
    let mut kids: Vec<(u8, u64)> = Vec::with_capacity(n);
    for idx in (0..cnt).rev() {
        let v = order[idx] as usize;
        kids.clear();
        for &w in &nbr[v] {
            if w != parent[v] {
                kids.push((len[w as usize], bits[w as usize]));
            }
        }
        kids.sort_unstable();
        let mut b: u64 = 1;
        let mut l: u8 = 1;
        for &(kl, kb) in &kids {
            b = (b << kl) | kb;
            l += kl;
        }
        b <<= 1;
        l += 1;
        bits[v] = b;
        len[v] = l;
    }
    bits[root]
}

fn code_unrooted(n: usize, nbr: &Vec<Vec<u8>>) -> u64 {
    // centres by stripping leaves
    let mut deg = [0usize; MAXN + 2];
    let mut layer: Vec<usize> = Vec::new();
    for v in 1..=n {
        deg[v] = nbr[v].len();
        if deg[v] <= 1 {
            layer.push(v);
        }
    }
    let mut left = n;
    while left > 2 {
        left -= layer.len();
        let mut nxt = Vec::new();
        for &v in &layer {
            for &w in &nbr[v] {
                let w = w as usize;
                if deg[w] > 1 {
                    deg[w] -= 1;
                    if deg[w] == 1 {
                        nxt.push(w);
                    }
                }
            }
            deg[v] = 0;
        }
        layer = nxt;
    }
    layer.iter().map(|&c| code_rooted(n, nbr, c)).min().unwrap()
}

fn bits_to_paren(b: u64, n: usize) -> String {
    let mut s = String::new();
    for i in (0..2 * n).rev() {
        s.push(if (b >> i) & 1 == 1 { '(' } else { ')' });
    }
    s
}

impl Enum {
    fn leaf(&mut self, mruns: u32, mbig: u32) {
        self.total += 1;
        let n = self.n;
        let mut nbr: Vec<Vec<u8>> = vec![Vec::new(); n + 1];
        for i in 0..self.ne {
            nbr[self.ea[i] as usize].push(self.eb[i]);
            nbr[self.eb[i] as usize].push(self.ea[i]);
        }
        let c = code_unrooted(n, &nbr);
        let skip: u8 = if mbig <= 1 { (mruns.max(1) - 1) as u8 } else { 255 };
        let e = self.shapes.entry(c).or_insert((0, 255, 255));
        e.0 += 1;
        e.1 = e.1.min(mruns as u8);
        e.2 = e.2.min(skip);
        self.anchors.insert(code_rooted(n, &nbr, 1));
    }
    fn rec(&mut self, k: usize, mruns: u32, mbig: u32) {
        if k == 0 {
            self.leaf(mruns, mbig);
            return;
        }
        for p in 1..=(self.n - k) {
            let ua = (self.used >> p) & 1;
            let ub = (self.used >> (p + k)) & 1;
            if ua + ub != 1 {
                continue;
            }
            let x = if ua == 1 { p + k } else { p };
            let (r, b) = runs_big(self.full & !self.used & !(1u64 << x));
            if r > self.maxruns || b > self.maxbig {
                continue;
            }
            self.used |= 1u64 << x;
            self.ea[self.ne] = p as u8;
            self.eb[self.ne] = (p + k) as u8;
            self.ne += 1;
            self.rec(k - 1, mruns.max(r), mbig.max(b));
            self.ne -= 1;
            self.used &= !(1u64 << x);
        }
    }
    // collect prefixes down to bracket length `stop` (exclusive)
    fn prefixes(&mut self, k: usize, stop: usize, mruns: u32, mbig: u32, out: &mut Vec<(Vec<(u8, u8)>, u64, u32, u32)>) {
        if k == stop || k == 0 {
            let e: Vec<(u8, u8)> = (0..self.ne).map(|i| (self.ea[i], self.eb[i])).collect();
            out.push((e, self.used, mruns, mbig));
            return;
        }
        for p in 1..=(self.n - k) {
            let ua = (self.used >> p) & 1;
            let ub = (self.used >> (p + k)) & 1;
            if ua + ub != 1 {
                continue;
            }
            let x = if ua == 1 { p + k } else { p };
            let (r, b) = runs_big(self.full & !self.used & !(1u64 << x));
            if r > self.maxruns || b > self.maxbig {
                continue;
            }
            self.used |= 1u64 << x;
            self.ea[self.ne] = p as u8;
            self.eb[self.ne] = (p + k) as u8;
            self.ne += 1;
            self.prefixes(k - 1, stop, mruns.max(r), mbig.max(b), out);
            self.ne -= 1;
            self.used &= !(1u64 << x);
        }
    }
}

fn new_enum(n: usize, maxruns: u32, maxbig: u32) -> Enum {
    Enum { n, full: ((1u64 << n) - 1) << 1, maxruns, maxbig, used: 0, ea: [0; MAXN], eb: [0; MAXN], ne: 0, shapes: HashMap::new(), anchors: HashSet::new(), total: 0 }
}

fn run_enum(n: usize, maxruns: u32, maxbig: u32, threads: usize) {
    assert!(n >= 2 && n <= 32);
    let mut e0 = new_enum(n, maxruns, maxbig);
    e0.used = (1u64 << 1) | (1u64 << n);
    e0.ea[0] = 1;
    e0.eb[0] = n as u8;
    e0.ne = 1;
    let mut pref = Vec::new();
    let stop = if n > 8 { n - 6 } else { 0 };
    e0.prefixes(n - 2, stop, 1, if n > 3 { 1 } else { 0 }, &mut pref);
    let pref = Arc::new(pref);
    let next = Arc::new(AtomicUsize::new(0));
    let mut handles = Vec::new();
    for _ in 0..threads {
        let pref = pref.clone();
        let next = next.clone();
        handles.push(std::thread::spawn(move || {
            let mut e = new_enum(n, maxruns, maxbig);
            loop {
                let i = next.fetch_add(1, Ordering::Relaxed);
                if i >= pref.len() {
                    break;
                }
                let (ref ed, used, mr, mb) = pref[i];
                e.used = used;
                e.ne = ed.len();
                for (j, &(a, b)) in ed.iter().enumerate() {
                    e.ea[j] = a;
                    e.eb[j] = b;
                }
                let k = n - 1 - ed.len();
                e.rec(k, mr, mb);
            }
            e
        }));
    }
    let mut shapes: HashMap<u64, (u64, u8, u8)> = HashMap::new();
    let mut anchors: HashSet<u64> = HashSet::new();
    let mut total = 0u64;
    for h in handles {
        let e = h.join().unwrap();
        total += e.total;
        for (c, v) in e.shapes {
            let s = shapes.entry(c).or_insert((0, 255, 255));
            s.0 += v.0;
            s.1 = s.1.min(v.1);
            s.2 = s.2.min(v.2);
        }
        anchors.extend(e.anchors);
    }
    let stdout = io::stdout();
    let mut out = io::BufWriter::new(stdout.lock());
    writeln!(out, "N {} placements {} shapes {} rooted_at_1 {}", n, total, shapes.len(), anchors.len()).unwrap();
    let mut keys: Vec<_> = shapes.iter().collect();
    keys.sort();
    for (c, v) in keys {
        writeln!(out, "T {} {} {} {}", bits_to_paren(*c, n), v.0, v.1, v.2).unwrap();
    }
    let mut a: Vec<_> = anchors.into_iter().collect();
    a.sort();
    for c in a {
        writeln!(out, "A {}", bits_to_paren(c, n)).unwrap();
    }
}

// ---------------------------------------------------------------- spiders (README 12, 13)

struct Deal {
    m: usize,
    legs: Vec<usize>,
    zig: bool,
    rule: u8, // 0 free order; 1 level by level; 2 first number of every leg first
    tip: Vec<usize>,
    done: Vec<usize>,
    lastup: Vec<bool>,
    used: u64,
    path: Vec<Vec<usize>>,
    nodes: u64,
}

impl Deal {
    fn rec(&mut self, w: usize) -> bool {
        if w == 0 {
            return true;
        }
        self.nodes += 1;
        let k = self.legs.len();
        let mut lowest = usize::MAX; // fewest numbers received among unfinished legs
        for i in 0..k {
            if self.done[i] < self.legs[i] {
                lowest = lowest.min(self.done[i]);
            }
        }
        for i in 0..k {
            if self.done[i] == self.legs[i] {
                continue;
            }
            if self.rule == 1 && self.done[i] != lowest {
                continue; // every leg gets its j-th number before any gets its (j+1)-th
            }
            if self.rule == 2 && self.done[i] > 0 && lowest == 0 {
                continue; // the first number of every leg comes first
            }
            // an untouched leg equal in length to an earlier untouched leg is the same choice
            if self.done[i] == 0 && i > 0 && self.legs[i - 1] == self.legs[i] && self.done[i - 1] == 0 {
                continue;
            }
            for dir in 0..2 {
                let up = dir == 0;
                if self.done[i] == 0 && !up {
                    continue; // first move of a leg is up, from 0
                }
                if self.zig && self.done[i] > 0 && up == self.lastup[i] {
                    continue;
                }
                let t = self.tip[i];
                let nt = if up { t + w } else { if t > w { t - w } else { continue } };
                if nt > self.m || (self.used >> nt) & 1 == 1 {
                    continue;
                }
                let (ot, ol) = (self.tip[i], self.lastup[i]);
                self.tip[i] = nt;
                self.lastup[i] = up;
                self.done[i] += 1;
                self.used |= 1u64 << nt;
                self.path[i].push(nt);
                if self.rec(w - 1) {
                    return true;
                }
                self.path[i].pop();
                self.used &= !(1u64 << nt);
                self.done[i] -= 1;
                self.tip[i] = ot;
                self.lastup[i] = ol;
            }
        }
        false
    }
}

fn partitions(m: usize, maxpart: usize, cur: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
    if m == 0 {
        if cur.len() >= 3 {
            out.push(cur.clone());
        }
        return;
    }
    for p in (1..=maxpart.min(m)).rev() {
        cur.push(p);
        partitions(m - p, p, cur, out);
        cur.pop();
    }
}

fn spider_line(legs: &Vec<usize>, zig: bool, rule: u8) -> String {
    let m: usize = legs.iter().sum();
    let k = legs.len();
    let mut d = Deal { m, legs: legs.clone(), zig, rule, tip: vec![0; k], done: vec![0; k], lastup: vec![false; k], used: 1, path: vec![Vec::new(); k], nodes: 0 };
    let head = legs.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(" ");
    if d.rec(m) {
        let body = d.path.iter().map(|p| p.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",")).collect::<Vec<_>>().join(" ; ");
        format!("{} | OK {}", head, body)
    } else {
        format!("{} | NONE", head)
    }
}

fn run_spiders(n: usize, zig: bool, rule: u8, threads: usize) {
    let mut parts = Vec::new();
    partitions(n - 1, n - 1, &mut Vec::new(), &mut parts);
    let parts = Arc::new(parts);
    let next = Arc::new(AtomicUsize::new(0));
    let mut handles = Vec::new();
    for _ in 0..threads {
        let parts = parts.clone();
        let next = next.clone();
        handles.push(std::thread::spawn(move || {
            let mut res = Vec::new();
            loop {
                let i = next.fetch_add(1, Ordering::Relaxed);
                if i >= parts.len() {
                    break;
                }
                res.push((i, spider_line(&parts[i], zig, rule)));
            }
            res
        }));
    }
    let mut all = Vec::new();
    for h in handles {
        all.extend(h.join().unwrap());
    }
    all.sort();
    for (_, s) in all {
        println!("{}", s);
    }
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let threads: usize = std::env::var("THREADS").ok().and_then(|s| s.parse().ok()).unwrap_or(4);
    let inf = |s: &str| -> u32 { if s == "inf" { u32::MAX } else { s.parse().unwrap() } };
    match a[1].as_str() {
        "solve" => run_stream("solve", inf(&a[2]), inf(&a[3]), threads),
        "minskip" => run_stream("minskip", 0, 0, threads),
        "minruns" => run_stream("minruns", 0, 0, threads),
        "anchors" => run_stream("anchors", 0, 0, threads),
        "enum" => run_enum(a[2].parse().unwrap(), inf(&a[3]), inf(&a[4]), threads),
        "spider" => run_spiders(a[2].parse().unwrap(), a[3] == "zig", match a[3].as_str() { "level" => 1, "first" => 2, _ => 0 }, threads),
        _ => eprintln!("unknown mode"),
    }
}
