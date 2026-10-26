"use client";

import { useState } from "react";
import Link from "next/link";

type PreviewRole = "aicte-admin" | "verifier";

const previewCopy: Record<PreviewRole, { title: string; subtitle: string }> = {
  "aicte-admin": {
    title: "AICTE Admin",
    subtitle: "National oversight preview",
  },
  verifier: {
    title: "Verifier / Employer",
    subtitle: "Student credential verification preview",
  },
};

export function DemoRolePreview({ role }: { role: PreviewRole }) {
  const [apaarId, setApaarId] = useState("");
  const [verificationAttempted, setVerificationAttempted] = useState(false);
  const isVerifier = role === "verifier";

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4">
          <Link href="/" className="text-lg font-extrabold tracking-tight text-[#0B2545]">
            APAAR
          </Link>
          <Link href="/" className="rounded-lg px-3 py-2 text-sm font-medium text-blue-700 hover:bg-blue-50">
            Back to login
          </Link>
        </div>
      </header>

      <div className="mx-auto max-w-6xl px-5 py-8 sm:py-12">
        <div className="mb-7 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">
          <span className="font-semibold">Read-only demo preview.</span> All information here is synthetic sample data. No account is signed in, and no real records are accessed or changed.
        </div>

        <div className="mb-8">
          <p className="mb-2 text-xs font-semibold uppercase tracking-[0.14em] text-blue-700">Role preview</p>
          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">{previewCopy[role].title}</h1>
          <p className="mt-2 text-sm text-slate-600">{previewCopy[role].subtitle}</p>
        </div>

        {isVerifier ? (
          <section className="max-w-2xl rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7" aria-labelledby="verify-heading">
            <h2 id="verify-heading" className="text-lg font-semibold">Verify a sample credential</h2>
            <p className="mt-1 text-sm text-slate-600">Use the sample ID shown below. This preview does not connect to APAAR or DigiLocker.</p>
            <form
              className="mt-6 space-y-3"
              onSubmit={(event) => {
                event.preventDefault();
                setVerificationAttempted(true);
              }}
            >
              <label htmlFor="demo-apaar-id" className="block text-sm font-medium text-slate-700">Sample APAAR ID</label>
              <div className="flex flex-col gap-2 sm:flex-row">
                <input
                  id="demo-apaar-id"
                  value={apaarId}
                  onChange={(event) => {
                    setApaarId(event.target.value);
                    setVerificationAttempted(false);
                  }}
                  placeholder="APAAR-DEMO-1001"
                  className="min-w-0 flex-1 rounded-lg border border-slate-300 px-3 py-2.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
                />
                <button type="submit" className="rounded-lg bg-blue-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
                  Check sample
                </button>
              </div>
              <p className="text-xs text-slate-500">Try: <button type="button" onClick={() => { setApaarId("APAAR-DEMO-1001"); setVerificationAttempted(false); }} className="font-medium text-blue-700 underline underline-offset-2">APAAR-DEMO-1001</button></p>
            </form>

            {verificationAttempted && (
              apaarId.trim().toUpperCase() === "APAAR-DEMO-1001" ? (
                <div className="mt-6 rounded-xl border border-emerald-200 bg-emerald-50 p-4" role="status">
                  <p className="text-sm font-semibold text-emerald-900">Sample credential found</p>
                  <dl className="mt-3 grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                    <div><dt className="text-xs text-slate-500">Student</dt><dd className="mt-0.5 font-medium text-slate-800">Demo Student</dd></div>
                    <div><dt className="text-xs text-slate-500">Institution</dt><dd className="mt-0.5 font-medium text-slate-800">XYZ College of Engineering</dd></div>
                    <div><dt className="text-xs text-slate-500">Credential status</dt><dd className="mt-0.5 font-medium text-emerald-800">Verified (sample)</dd></div>
                    <div><dt className="text-xs text-slate-500">APAAR ID</dt><dd className="mt-0.5 font-medium text-slate-800">APAAR-DEMO-1001</dd></div>
                  </dl>
                  <p className="mt-3 text-xs text-emerald-800">This is a local preview result, not an official verification.</p>
                </div>
              ) : (
                <p className="mt-5 rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-600" role="status">No matching sample. Try APAAR-DEMO-1001.</p>
              )
            )}
          </section>
        ) : (
          <>
            <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4" aria-label="Sample national metrics">
              {[
                ["Institutions", "1,248", "+ 18 this month"],
                ["Student records", "7,42,860", "Across sample data"],
                ["Validated", "96.4%", "Sample validation rate"],
                ["Needs review", "2,681", "Sample flagged records"],
              ].map(([label, value, note]) => (
                <article key={label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                  <h2 className="text-sm font-medium text-slate-500">{label}</h2>
                  <p className="mt-3 text-3xl font-bold tracking-tight text-slate-900">{value}</p>
                  <p className="mt-2 text-xs text-slate-500">{note}</p>
                </article>
              ))}
            </section>
            <section className="mt-6 grid gap-4 lg:grid-cols-3">
              <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm lg:col-span-2">
                <h2 className="text-base font-semibold">Sample regional coverage</h2>
                <p className="mt-1 text-sm text-slate-500">Illustrative institution counts by region</p>
                <div className="mt-5 space-y-4">
                  {[["Western", 82], ["Southern", 74], ["Northern", 68], ["Eastern", 53]].map(([region, count]) => (
                    <div key={region}>
                      <div className="mb-1.5 flex justify-between text-sm"><span className="text-slate-700">{region}</span><span className="font-medium text-slate-900">{count} institutions</span></div>
                      <div className="h-2 rounded-full bg-slate-100"><div className="h-2 rounded-full bg-blue-600" style={{ width: `${Number(count) / 100 * 100}%` }} /></div>
                    </div>
                  ))}
                </div>
              </article>
              <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <h2 className="text-base font-semibold">Recent sample activity</h2>
                <ul className="mt-4 space-y-4 text-sm">
                  <li className="border-l-2 border-emerald-400 pl-3"><p className="font-medium">Batch validation complete</p><p className="mt-0.5 text-xs text-slate-500">XYZ College · 5 minutes ago</p></li>
                  <li className="border-l-2 border-blue-400 pl-3"><p className="font-medium">Institution profile updated</p><p className="mt-0.5 text-xs text-slate-500">Sample record · 1 hour ago</p></li>
                  <li className="border-l-2 border-amber-400 pl-3"><p className="font-medium">Records flagged for review</p><p className="mt-0.5 text-xs text-slate-500">Sample validation · 3 hours ago</p></li>
                </ul>
              </article>
            </section>
          </>
        )}
      </div>
    </main>
  );
}
