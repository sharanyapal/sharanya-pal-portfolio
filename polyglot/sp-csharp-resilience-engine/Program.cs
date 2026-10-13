using System.Collections.Concurrent;
using System.Threading.Channels;

// Queue-based async worker pool with bounded buffers and retry/backoff.
// Simulated jobs; replace ProcessAsync with a real dependency only after adding idempotency.
var queue = Channel.CreateBounded<Job>(new BoundedChannelOptions(16) { FullMode = BoundedChannelFullMode.Wait });
var results = new ConcurrentBag<(int Id, bool Ok, int Attempts)>();
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(15));
var workers = Enumerable.Range(0, 3).Select(_ => Worker(queue.Reader, results, cts.Token)).ToArray();
foreach (int id in Enumerable.Range(1, 24)) await queue.Writer.WriteAsync(new Job(id, 0), cts.Token);
queue.Writer.Complete();
await Task.WhenAll(workers);
Console.WriteLine($"Processed {results.Count} jobs; succeeded {results.Count(x => x.Ok)}; max attempts {results.Max(x=>x.Attempts)}");
if (results.Count != 24 || results.Any(x => !x.Ok)) throw new Exception("unexpected worker result");

static async Task Worker(ChannelReader<Job> reader, ConcurrentBag<(int Id, bool Ok, int Attempts)> results, CancellationToken ct)
{
    await foreach (var job in reader.ReadAllAsync(ct))
    {
        bool success = false;
        int attempt = 0;
        while (attempt < 4 && !success)
        {
            attempt++;
            try
            {
                await SimulateRemoteCall(job.Id, attempt, ct);
                success = true;
            }
            catch (HttpRequestException) when (attempt < 4)
            {
                await Task.Delay(TimeSpan.FromMilliseconds(Math.Min(200, 20 * (1 << attempt))), ct);
            }
        }
        results.Add((job.Id, success, attempt));
    }
}
static async Task SimulateRemoteCall(int id, int attempt, CancellationToken ct)
{
    await Task.Delay(8, ct);
    if (id % 5 == 0 && attempt < 3) throw new HttpRequestException("transient upstream unavailable");
}
record Job(int Id, int Retry);
