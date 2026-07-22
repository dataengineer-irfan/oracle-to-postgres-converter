import { useState, useEffect, useRef } from 'react';
import client from '../api/client';

/**
 * useLiveData hook
 * Polls an endpoint on a timer and returns { data, loading, error, refetch }
 * 
 * @param {string}  url      - API endpoint URL
 * @param {number}  interval - polling interval in ms (0 = no polling, fetch once)
 * @param {any}     fallback - value to return while loading or on error
 */
export function useLiveData(url, interval = 0, fallback = null) {
  const [data, setData]       = useState(fallback);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);
  const timerRef              = useRef(null);
  const mountedRef            = useRef(true);

  const fetch = async () => {
    try {
      const res = await client.get(url);
      if (mountedRef.current) {
        setData(res.data);
        setError(null);
      }
    } catch (err) {
      if (mountedRef.current) {
        setError(err?.message ?? 'Error');
        // Keep last good data on error — don't reset to fallback
      }
    } finally {
      if (mountedRef.current) setLoading(false);
    }
  };

  useEffect(() => {
    mountedRef.current = true;
    fetch();

    if (interval > 0) {
      timerRef.current = setInterval(fetch, interval);
    }

    return () => {
      mountedRef.current = false;
      if (timerRef.current) clearInterval(timerRef.current);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url]);

  return { data, loading, error, refetch: fetch };
}
